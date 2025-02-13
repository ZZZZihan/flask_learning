<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Edit, Delete } from '@element-plus/icons-vue'
import { useAuthStore } from '@/stores/auth'
import request from '@/utils/request'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const achievement = ref(null)
const loading = ref(false)

const fetchAchievement = async () => {
  try {
    loading.value = true
    const res = await request({
      url: `/achievements/${route.params.id}`,
      method: 'get'
    })
    achievement.value = res
  } catch (error) {
    ElMessage.error('获取成就详情失败')
    router.push('/achievements')
  } finally {
    loading.value = false
  }
}

const handleEdit = () => {
  router.push(`/achievements/${achievement.value.id}/edit`)
}

const handleDelete = async () => {
  try {
    await ElMessageBox.confirm('确定要删除这个成就吗？', '提示', {
      type: 'warning'
    })
    
    await request({
      url: `/achievements/${achievement.value.id}`,
      method: 'delete'
    })
    
    ElMessage.success('删除成功')
    router.push('/achievements')
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const canEdit = computed(() => {
  return authStore.user?.id === achievement.value?.user.id
})

onMounted(() => {
  fetchAchievement()
})
</script>

<template>
  <div class="achievement-detail" v-loading="loading">
    <template v-if="achievement">
      <div class="page-header">
        <h2>{{ achievement.title }}</h2>
        <div class="actions" v-if="canEdit">
          <el-button
            type="primary"
            :icon="Edit"
            @click="handleEdit"
          >
            编辑
          </el-button>
          <el-button
            type="danger"
            :icon="Delete"
            @click="handleDelete"
          >
            删除
          </el-button>
        </div>
      </div>

      <el-card>
        <template #header>
          <div class="card-header">
            <span class="category">分类：{{ achievement.category }}</span>
            <div class="meta">
              <span>作者：{{ achievement.user.username }}</span>
              <span>创建时间：{{ achievement.created_at }}</span>
              <span>浏览量：{{ achievement.views }}</span>
            </div>
          </div>
        </template>

        <div class="content">
          <div class="description">
            {{ achievement.description }}
          </div>

          <div class="attachments" v-if="achievement.file_url">
            <h3>附件</h3>
            <el-link
              :href="achievement.file_url"
              type="primary"
              target="_blank"
            >
              下载附件
            </el-link>
          </div>
        </div>
      </el-card>
    </template>
  </div>
</template>

<style scoped lang="scss">
.achievement-detail {
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

    .actions {
      display: flex;
      gap: 10px;
    }
  }

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;

    .category {
      font-size: 16px;
      color: #409eff;
    }

    .meta {
      display: flex;
      gap: 20px;
      color: #909399;
      font-size: 14px;
    }
  }

  .content {
    .description {
      font-size: 16px;
      line-height: 1.6;
      color: #606266;
      white-space: pre-wrap;
    }

    .attachments {
      margin-top: 30px;
      padding-top: 20px;
      border-top: 1px solid #dcdfe6;

      h3 {
        margin: 0 0 10px;
        font-size: 18px;
        color: #303133;
      }
    }
  }
}
</style>
 