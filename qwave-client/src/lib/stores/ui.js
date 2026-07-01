import { writable } from "svelte/store";

export const activePanel = writable("null")
export const activeTab = writable("nav")
export const tabMeta = writable("null")

export function openUtility(name) {
  activeTab.set(name)
}
