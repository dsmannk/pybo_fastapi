import qs from "qs"
import { access_token, username, is_login } from "./store.js";
import { get } from 'svelte/store'
import { push } from 'svelte-spa-router'

// operation =	데이터를 처리하는 방법, 소문자만 사용한다.	(get, post, put, delete)
// url	= 요청 URL, 단 백엔드 서버의 호스트명 이후의 URL만 전달 (ex) /api/question/list
// params =	요청 데이터	{page: 1, keyword: "마크다운" }
// success_callback = API 호출 성공시 수행할 함수, 전달된 함수에는 API 호출시 리턴되는 json이 입력으로 주어진다.
// failure_callback	= API 호출 실패시 수행할 함수, 전달된 함수에는 오류 값이 입력으로 주어진다.
const fastapi = (operation, url, params, success_callback, failure_callback) => {
    let method = operation
    let content_type = 'application/json'
    let body = JSON.stringify(params)

    // OAuth2를 사용하여 로그인 할때 Content-Type을 application/x-www-form-urlencoded로 사용해야 하는 것은 OAuth2의 규칙이다.
    // body에 설정한 qs.stringify(params)는 params 데이터를 'application/x-www-form-urlencoded' 형식에 맞게끔 변환하는 역할을 한다.
    // qs.stringify 함수를 사용하기 위해서는 다음과 같이 qs 패키지를 먼저 설치해야 한다.
    if(operation === 'login') {
        method = 'post'
        content_type = 'application/x-www-form-urlencoded'
        body = qs.stringify(params)
    }

    let _url = import.meta.env.VITE_SERVER_URL+url
    if(method === 'get') {
        _url += "?" + new URLSearchParams(params)
    }

    console.log(_url)

    let options = {
        method: method,
        headers: {
            "Content-Type": content_type
        }
    }

    const _access_token = get(access_token)
    if (_access_token) {
        options.headers["Authorization"] = "Bearer " + _access_token
    }

    if (method !== 'get') {
        options['body'] = body
    }

    fetch(_url, options)
        .then(response => {
            if(response.status === 204) { // No content
                if(success_callback) {
                    success_callback()
                }
                return
            }
            response.json()
                .then(json => {
                    if(response.status >= 200 && response.status < 300) { // 200 ~ 299
                        if (success_callback) {
                            success_callback(json)
                        }
                    } else if(operation !== 'login' && response.status === 401) { // token timeout
                        access_token.set('')
                        username.set('')
                        is_login.set(false)
                        alert("로그인이 필요합니다.")
                        push('/user-login')
                    } else {
                        if (failure_callback) {
                            failure_callback(json)
                        } else {
                            alert(JSON.stringify(json))
                        }
                    }
                })
                .catch(error => {
                    alert(JSON.stringify(error))
                })

        })
}

export default fastapi