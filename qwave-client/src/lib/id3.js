function encodeString(str) {
  return new TextEncoder().encode(str)
}

function makeFrame(id, value) {
  const data = encodeString(value)

  // header: 4 character tag id, 4 byte size, 2 byte flags, 1 byte encoding
  const buffer = new Uint8Array(10 + 1 + data.length)
  for (let i = 0; i < 4; i++) buffer[i] = id.charCodeAt(i) // tag id (ex. TIT2)
  const size = data.length + 1
  buffer[4] = (size >> 24) & 0x7f // size
  buffer[5] = (size >> 16) & 0x7f
  buffer[6] = (size >> 8)  & 0x7f
  buffer[7] = size         & 0x7f
  buffer[8] = 0; buffer[9] = 0 // flags
  buffer[10] = 3 // utf-8 byte
  buffer.set(data, 11)
  return buffer
}

export async function writeID3(file, meta) {
  const frames = []
  if (meta.title)  frames.push(makeFrame("TIT2", meta.title))
  if (meta.artist) frames.push(makeFrame("TPE1", meta.artist))
  if (meta.album)  frames.push(makeFrame("TALB", meta.album))
  if (meta.track)  frames.push(makeFrame("TRCK", meta.track))
  if (meta.year)   frames.push(makeFrame("TDRC", meta.year))

  const framesSize = frames.reduce((n, f) => n + f.length, 0)

  // "ID3", version, flags, size | frames | audio content
  const header = new Uint8Array(10)
  header[0] = 0x49; header[1] = 0x44; header[2] = 0x33  // "ID3"
  header[3] = 0x04; header[4] = 0x00 //v2.4
  header[5] = 0x00 // no flags
  header[6] = (framesSize >> 21) & 0x7f
  header[7] = (framesSize >> 14) & 0x7f
  header[8] = (framesSize >> 7) & 0x7f
  header[9] = framesSize & 0x7f

  const original = await file.arrayBuffer()
  const tagged = new Blob([header, ...frames, original], { type: file.type })
  return new File([tagged], file.name, { type: file.type })
}
