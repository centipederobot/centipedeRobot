import axios from './axios'
import { endpoints } from './endpoints'

export const startHotspot = () => axios.post(endpoints.hotspot.start)
export const stopHotspot = () => axios.post(endpoints.hotspot.stop)
export const getHotspotStatus = () => axios.get(endpoints.hotspot.status)
