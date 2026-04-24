import { writable, derived, get } from "svelte/store"

export const queue =      writable([])
export const queueIndex = writable(0)
export const playing =    writable(false)
export const progress =   writable(0)
export const duration =   writable(0)
export const volume =     writable(1) //0-1

export const currentTrack = derived(
  [queue, queueIndex],
  ([$queue, $queueIndex]) => $queue[$queueIndex] ?? null
)

export function play(tracks, index = 0) {
  queue.set(tracks)
  queueIndex.set(index)
  playing.set(true)
}

export function playNext(track) {
  queue.update(q => {
    const i = get(queueIndex)
    const next = [...q]
    next.splice(i + 1, 0, track)
    return next
  })
}

export function queueItem(track) {
  queue.update(q => [...q, track])
}

export function skip(index) {
  queueIndex.set(index)
  playing.set(true)
}

export function next() {
  queue.update(q => {
    queueIndex.update(i => Math.min(i + 1, q.length - 1))
    return q
  })
  playing.set(true)
}

export function prev() {
  queueIndex.update(i => Math.max(i - 1, 0))
  playing.set(true)
}
