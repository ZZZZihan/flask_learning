import request from '@/utils/request'

export function getAchievements(params) {
  return request({
    url: '/achievements',
    method: 'get',
    params
  })
}

export function getAchievement(id) {
  return request({
    url: `/achievements/${id}`,
    method: 'get'
  })
}

export function createAchievement(data) {
  return request({
    url: '/achievements',
    method: 'post',
    data,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

export function updateAchievement(id, data) {
  return request({
    url: `/achievements/${id}`,
    method: 'put',
    data,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

export function deleteAchievement(id) {
  return request({
    url: `/achievements/${id}`,
    method: 'delete'
  })
}

export function getCategories() {
  return request({
    url: '/achievements/categories',
    method: 'get'
  })
}

export function getStats() {
  return request({
    url: '/achievements/stats',
    method: 'get'
  })
} 