import axios from 'axios'

const instance = axios.create({
    baseURL: 'http://localhost:8000', // آدرس بک‌اند FastAPI
    timeout: 5000,
    headers: {
        'Content-Type': 'application/json',
    },
})

export default instance
