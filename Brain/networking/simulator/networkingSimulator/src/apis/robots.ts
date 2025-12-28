import axios from './axios'
import { endpoints } from './endpoints'

export const sendRobotCommand = (robotId: string, payload: any) => {
    return axios.post(endpoints.robotCommand(robotId), payload)
}

export const getRobotStatus = (robotId: string) => {
    return axios.get(endpoints.robotStatus(robotId))
}
