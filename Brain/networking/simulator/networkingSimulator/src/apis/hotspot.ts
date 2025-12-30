import axios from './axios'
import { endpoints } from './endpoints'

export const startHotspot = (id: string) => axios.post(endpoints.hotspot.start(id))
export const stopHotspot = (id: string) => axios.post(endpoints.hotspot.stop(id))
export const getHotspotStatus = (id: string) => axios.get(endpoints.hotspot.status(id))
