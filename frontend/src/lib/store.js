import { writable } from 'svelte/store'

const persist_storage = (key, initValue) => {
    const storedValueStr = localStorage.getItem(key)
    const store = writable(storedValueStr != null ? JSON.parse(storedValueStr) : initValue)
    store.subscribe((val) => {
        localStorage.setItem(key, JSON.stringify(val))
    })
    return store
}

// 스벨트 스토어 - https://svelte.dev/tutorial/writable-stores
export const page = persist_storage("page", 0)
export const keyword = persist_storage("keyword", "")
// 3가지 로그인 정보는 브라우저를 새로고침 하더라도 유지
//  - access_token - 액세스 토큰
//  - username - 사용자명
//  - is_login - 로그인 여부
export const access_token = persist_storage("access_token", "")
export const username = persist_storage("username", "")
export const is_login = persist_storage("is_login", false)


