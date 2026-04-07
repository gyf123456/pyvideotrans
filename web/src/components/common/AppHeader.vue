<template>
  <el-header class="app-header">
    <div class="header-left">
      <h1 class="logo">pyVideoTrans</h1>
      <el-menu mode="horizontal" :ellipsis="false" class="nav-menu" :default-active="currentRoute">
        <el-menu-item index="/" @click="$router.push('/')">
          <el-icon><VideoPlay /></el-icon>
          工作区
        </el-menu-item>
        <el-menu-item index="/tasks" @click="$router.push('/tasks')">
          <el-icon><List /></el-icon>
          任务列表
        </el-menu-item>
        <el-menu-item index="/settings" @click="$router.push('/settings')">
          <el-icon><Setting /></el-icon>
          设置
        </el-menu-item>
      </el-menu>
    </div>
    <div class="header-right">
      <DarkModeToggle />
    </div>
  </el-header>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import DarkModeToggle from './DarkModeToggle.vue'

const route = useRoute()

const currentRoute = computed(() => route.path)
</script>

<style scoped>
.app-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  border-bottom: 1px solid var(--el-border-color);
  height: 60px;
  background: var(--el-bg-color);
}
.header-left {
  display: flex;
  align-items: center;
  gap: 20px;
}
.logo {
  font-size: 18px;
  margin: 0;
  white-space: nowrap;
  color: var(--el-color-primary);
}
.nav-menu {
  border-bottom: none !important;
}
.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}
</style>
