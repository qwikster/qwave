import { writable } from "svelte/store";

export const activePanel = writable("null")
export const activeTab = writable("login")

export function openUtility(name) {
  activeTab.set(name)
}
