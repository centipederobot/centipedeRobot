import axios from './axios'
import { endpoints } from './endpoints'

export const sendGroupCommand = (payload: {
    robotLeaderId: string,
    cmds: { robotId: string, cmd: string, value: number[], timeStamp: string }[],
    timeStamp: string
}, robotLeaderId: string) => axios.post(endpoints.groupCommand(robotLeaderId), payload)
