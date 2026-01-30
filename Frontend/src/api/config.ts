import axios from "axios"

const service = axios.create({
    baseURL: "/api",
    withCredentials: true,
})

// 请求拦截器
service.interceptors.request.use(
    config => {
        if (localStorage.getItem("token")) {
            config.headers["Authorization"] = "Token " + localStorage.getItem("token");
        }

        return config
    },
    error => {
        console.log(error)
        return Promise.reject(error)
    }
)

export default service
