<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Search, Plus } from '@element-plus/icons-vue'
import request from '@/utils/request'

const router = useRouter()
const achievements = ref([])
const categories = ref([])
const loading = ref(false)
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)

const searchForm = ref({
  query: '',
  category: ''
})

const fetchAchievements = async () => {
  try {
    loading.value = true
    const params = {
      page: currentPage.value,
      per_page: pageSize.value,
      ...searchForm.value
    }
    const res = await request({
      url: '/achievements',
      method: 'get',
      params
    })
    achievements.value = res.items
    total.value = res.total
  } catch (error) {
    ElMessage.error('获取成就列表失败')
  } finally {
    loading.value = false
  }
}

const fetchCategories = async () => {
  try {
    const res = await request({
      url: '/achievements/categories',
      method: 'get'
    })
    categories.value = res
  } catch (error) {
    ElMessage.error('获取分类列表失败')
  }
}

const handleSearch = () => {
  currentPage.value = 1
  fetchAchievements()
}

const handlePageChange = (page) => {
  currentPage.value = page
  fetchAchievements()
}

const handleSizeChange = (size) => {
  pageSize.value = size
  currentPage.value = 1
  fetchAchievements()
}

const handleViewAchievement = (id) => {
  router.push(`/achievements/${id}`)
}

onMounted(() => {
  fetchAchievements()
  fetchCategories()
})
</script>

<template>
  <div class="achievement-list">
    <div class="page-header">
      <h2>成就列表</h2>
      <el-button
        type="primary"
        :icon="Plus"
        @click="router.push('/achievements/new')"
      >
        新建成就
      </el-button>
    </div>

    <el-card class="filter-card">
      <el-form :inline="true" :model="searchForm" @submit.prevent="handleSearch">
        <el-form-item>
          <el-input
            v-model="searchForm.query"
            placeholder="搜索成就"
            :prefix-icon="Search"
            clearable
          />
        </el-form-item>
        
        <el-form-item>
          <el-select
            v-model="searchForm.category"
            placeholder="选择分类"
            clearable
          >
            <el-option
              v-for="category in categories"
              :key="category"
              :label="category"
              :value="category"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" native-type="submit">搜索</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card v-loading="loading">
      <el-table :data="achievements" style="width: 100%">
        <el-table-column prop="title" label="标题" min-width="200">
          <template #default="{ row }">
            <el-link
              type="primary"
              :underline="false"
              @click="handleViewAchievement(row.id)"
            >
              {{ row.title }}
            </el-link>
          </template>
        </el-table-column>
        <el-table-column prop="category" label="分类" width="120" />
        <el-table-column prop="views" label="浏览量" width="100" align="center" />
        <el-table-column prop="created_at" label="创建时间" width="180" />
        <el-table-column
          prop="user.username"
          label="创建者"
          width="120"
          align="center"
        />
      </el-table>

      <div class="pagination-container">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50]"
          :total="total"
          layout="total, sizes, prev, pager, next"
          @size-change="handleSizeChange"
          @current-change="handlePageChange"
        />
      </div>
    </el-card>
  </div>
</template>

<style scoped lang="scss">
.achievement-list {
  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;

    h2 {
      margin: 0;
      font-size: 24px;
      color: #303133;
    }
  }

  .filter-card {
    margin-bottom: 20px;
  }

  .pagination-container {
    display: flex;
    justify-content: center;
    margin-top: 20px;
  }
}
</style> 