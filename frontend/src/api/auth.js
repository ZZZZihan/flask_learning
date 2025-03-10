import request from '@/utils/request'

export function login(data) {
  return request({
    url: '/auth/login',
    method: 'post',
    data
  })
}

export function register(data) {
  return request({
    url: '/auth/register',
    method: 'post',
    data
  })
}

export function getInfo() {
  return request({
    url: '/auth/me',
    method: 'get'
  })
}

export function refreshToken() {
  return request({
    url: '/auth/refresh',
    method: 'post'
  })
} 