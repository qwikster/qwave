import { writable, derived } from "svelte/store"

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
