import axios from './axios'
import { endpoints } from './endpoints'

export const sendOffer = (robotId: string, payload: any) => {
    return axios.post(endpoints.webrtc.offer(robotId), payload)
}

export const getWebRTCStatus = (robotId: string) => {
    return axios.get(endpoints.webrtc.status(robotId))
}
