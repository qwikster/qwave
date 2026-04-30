export const audio = new Audio()
export const audioctx = new AudioContext()

const source = audioctx.createMediaElementSource(audio)
export const analyser = audioctx.createAnalyser()

source.connect(analyser)
analyser.connect(audioctx.destination)
