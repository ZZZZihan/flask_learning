<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElCard } from 'element-plus'
import request from '@/utils/request'

const router = useRouter()
const stats = ref({
  total: 0,
  monthly: 0,
  views: 0,
  files: 0
})
const loading = ref(false)
const recentAchievements = ref([])

const fetchStats = async () => {
  try {
    const res = await request({
      url: '/achievements/stats',
      method: 'get'
    })
    stats.value = res
  } catch (error) {
    console.error('获取统计数据失败:', error)
  }
}

const fetchRecentAchievements = async () => {
  try {
    loading.value = true
    const res = await request({
      url: '/achievements',
      method: 'get',
      params: {
        page: 1,
        per_page: 5
      }
    })
    recentAchievements.value = res.items
  } catch (error) {
    console.error('获取最新成就失败:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchStats()
  fetchRecentAchievements()
})
</script>

<template>
  <div class="home">
    <div class="welcome-section">
      <h1>欢迎来到成就系统</h1>
      <p class="subtitle">记录和分享你的成就</p>
    </div>

    <div class="stats-section">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-card class="stat-card">
            <h3>总成就数</h3>
            <div class="stat-value">{{ stats.total }}</div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stat-card">
            <h3>本月新增</h3>
            <div class="stat-value">{{ stats.monthly }}</div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stat-card">
            <h3>总浏览量</h3>
            <div class="stat-value">{{ stats.views }}</div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stat-card">
            <h3>文件数量</h3>
            <div class="stat-value">{{ stats.files }}</div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <div class="recent-section">
      <h2>最新成就</h2>
      <el-card v-loading="loading">
        <div v-if="recentAchievements.length" class="achievement-list">
          <div
            v-for="achievement in recentAchievements"
            :key="achievement.id"
            class="achievement-item"
            @click="router.push(`/achievements/${achievement.id}`)"
          >
            <h3>{{ achievement.title }}</h3>
            <div class="achievement-meta">
              <span>{{ achievement.category }}</span>
              <span>{{ achievement.user.username }}</span>
              <span>{{ achievement.created_at }}</span>
            </div>
          </div>
        </div>
        <div v-else class="empty-text">
          暂无成就
        </div>
      </el-card>
    </div>
  </div>
</template>

<style scoped lang="scss">
.home {
  .welcome-section {
    text-align: center;
    margin-bottom: 40px;

    h1 {
      font-size: 36px;
      color: #303133;
      margin: 0;
    }

    .subtitle {
      font-size: 18px;
      color: #606266;
      margin-top: 10px;
    }
  }

  .stats-section {
    margin-bottom: 40px;

    .stat-card {
      text-align: center;
      cursor: pointer;
      transition: transform 0.3s;

      &:hover {
        transform: translateY(-5px);
      }

      h3 {
        font-size: 16px;
        color: #606266;
        margin: 0 0 10px;
      }

      .stat-value {
        font-size: 24px;
        color: #409eff;
        font-weight: bold;
      }
    }
  }

  .recent-section {
    h2 {
      font-size: 24px;
      color: #303133;
      margin: 0 0 20px;
    }

    .achievement-list {
      .achievement-item {
        padding: 15px;
        border-bottom: 1px solid #ebeef5;
        cursor: pointer;
        transition: background-color 0.3s;

        &:last-child {
          border-bottom: none;
        }

        &:hover {
          background-color: #f5f7fa;
        }

        h3 {
          margin: 0 0 10px;
          font-size: 18px;
          color: #303133;
        }

        .achievement-meta {
          display: flex;
          gap: 20px;
          color: #909399;
          font-size: 14px;
        }
      }
    }

    .empty-text {
      text-align: center;
      padding: 30px;
      color: #909399;
      font-size: 14px;
    }
  }
}
</style> 