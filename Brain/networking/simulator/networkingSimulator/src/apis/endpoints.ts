export const endpoints = {
    robotCommand: (id: string) => `/robot/${id}/command`,
    robotStatus: (id: string) => `/robot/${id}/status`,
    groupCommand: (id: string) => `/group/command/${id}`,
    hotspot: {
        start: (id: string) => `/hotspot/${id}/start`,
        stop: (id: string) => `/hotspot/${id}/stop`,
        status: (id: string) => `/hotspot/${id}/status`,
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
