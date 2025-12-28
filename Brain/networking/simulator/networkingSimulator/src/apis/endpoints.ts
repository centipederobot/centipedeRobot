export const endpoints = {
    robotCommand: (id: string) => `/robot/${id}/command`,
    robotStatus: (id: string) => `/robot/${id}/status`,
    groupCommand: '/group/command',
    hotspot: {
        start: '/hotspot/start',
        stop: '/hotspot/stop',
        status: '/hotspot/status',
    },
    webrtc: {
        offer: (id: string) => `/webrtc/${id}/offer`,
        status: (id: string) => `/webrtc/${id}/status`,
    },
    commands: {
        list: '/commands/list',
        logs: '/commands/logs',
    },
}
