import axios from './axios'
import { endpoints } from './endpoints'

export const getCommandList = () => axios.get(endpoints.commands.list)
export const getCommandLogs = () => axios.get(endpoints.commands.logs)
