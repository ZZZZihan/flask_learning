<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Upload } from '@element-plus/icons-vue'
import request from '@/utils/request'
import { achievementTitleRules, achievementDescriptionRules, fileUploadRules } from '@/utils/validation'
import { useAppStore } from '@/stores/app'

const router = useRouter()
const route = useRoute()
const appStore = useAppStore()
const isEdit = computed(() => route.name === 'edit-achievement')
const loading = ref(false)
const categories = ref([])

const achievementForm = ref({
  title: '',
  description: '',
  category: '',
  file: null
})

const rules = {
  title: achievementTitleRules,
  description: achievementDescriptionRules,
  category: [
    { required: true, message: '请选择分类', trigger: 'change' }
  ]
}

const formRef = ref()
const fileRef = ref()

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

const fetchAchievement = async () => {
  try {
    loading.value = true
    const res = await request({
      url: `/achievements/${route.params.id}`,
      method: 'get'
    })
    achievementForm.value = {
      title: res.title,
      description: res.description,
      category: res.category,
      file: null
    }
  } catch (error) {
    ElMessage.error('获取成就详情失败')
    router.push('/achievements')
  } finally {
    loading.value = false
  }
}

const handleFileChange = (file) => {
  achievementForm.value.file = file.raw
}

const handleSubmit = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    
    loading.value = true
    const formData = new FormData()
    formData.append('title', achievementForm.value.title)
    formData.append('description', achievementForm.value.description)
    formData.append('category', achievementForm.value.category)
    if (achievementForm.value.file) {
      formData.append('file', achievementForm.value.file)
    }
    
    if (isEdit.value) {
      await request({
        url: `/achievements/${route.params.id}`,
        method: 'put',
        data: formData,
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      ElMessage.success('更新成功')
    } else {
      await request({
        url: '/achievements',
        method: 'post',
        data: formData,
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      ElMessage.success('创建成功')
    }
    
    router.push('/achievements')
  } catch (error) {
    if (error.name !== 'ValidationError') {
      ElMessage.error(isEdit.value ? '更新失败' : '创建失败')
    }
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchCategories()
  if (isEdit.value) {
    fetchAchievement()
  }
})
</script>

<template>
  <div class="achievement-form" v-loading="loading">
    <div class="page-header">
      <h2>{{ isEdit ? '编辑成就' : '新建成就' }}</h2>
    </div>

    <el-card>
      <el-form
        ref="formRef"
        :model="achievementForm"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="标题" prop="title">
          <el-input v-model="achievementForm.title" />
        </el-form-item>

        <el-form-item label="描述" prop="description">
          <el-input
            v-model="achievementForm.description"
            type="textarea"
            :rows="6"
          />
        </el-form-item>

        <el-form-item label="分类" prop="category">
          <el-select v-model="achievementForm.category" placeholder="选择分类">
            <el-option
              v-for="category in categories"
              :key="category"
              :label="category"
              :value="category"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="附件">
          <el-upload
            ref="fileRef"
            class="upload-demo"
            :auto-upload="false"
            :limit="1"
            :on-change="handleFileChange"
          >
            <template #trigger>
              <el-button type="primary" :icon="Upload">选择文件</el-button>
            </template>
            <template #tip>
              <div class="el-upload__tip">
                支持任意类型文件
              </div>
            </template>
          </el-upload>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="handleSubmit">
            {{ isEdit ? '更新' : '创建' }}
          </el-button>
          <el-button @click="router.back()">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<style scoped lang="scss">
.achievement-form {
  .page-header {
    margin-bottom: 20px;

    h2 {
      margin: 0;
      font-size: 24px;
      color: #303133;
    }
  }

  .upload-demo {
    :deep(.el-upload-list) {
      margin-top: 10px;
    }
  }
}
</style> 