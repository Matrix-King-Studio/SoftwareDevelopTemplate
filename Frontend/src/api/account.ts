import service from "./config";


interface LoginData {
    username: string;
    password: string;
}

interface RegistrationData {
    username: string;
    password1: string;
    password2: string;
    email: string;
}

export default {
    login(data: LoginData) {
        return service({
            url: `/account/rest-auth/login/`,
            method: "post",
            data
        })
    },
    getUserDetail() {
        return service({
            url: `/account/rest-auth/user/`,
            method: "get"
        })
    },
    register(data: RegistrationData) {
        return service({
            url: `/account/rest-auth/registration/`,
            method: "post",
            data
        })
    },
}
