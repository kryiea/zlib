<template>
  <div class="search-bar mb-4">
    <div class="card shadow-sm">
      <div class="card-body">
        <h4 class="card-title mb-4 text-primary">🔍</h4>
        <div class="form-group">
          <div class="input-group mb-3">
            <input
              v-model="searchInput"
              type="text"
              class="form-control form-control-lg"
              placeholder="输入书名或ISBN码"
              @keyup.enter="handleSearch"
            />
            <button
              @click="handleSearch"
              class="btn btn-primary btn-lg"
              :disabled="!isValidInput"
            >
              <i class="bi bi-search me-1"></i>
              搜索
            </button>
          </div>
          <div v-if="error" class="alert alert-danger mt-2">
            {{ error }}
          </div>
          <small class="form-text text-muted">
            支持书名或ISBN码（10位或13位数字）搜索
          </small>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  name: 'SearchBar',
  data() {
    return {
      searchInput: '',
      error: '',
      currentRequest: null,
      debounceTimeout: null,
      isSearching: false
    };
  },
  computed: {
    isValidInput() {
      return this.searchInput.trim() && !this.error;
    }
  },
  watch: {
    searchInput(newValue) {
      this.validateInput(newValue);
    }
  },
  methods: {
    validateInput(value) {
      const trimmedValue = value.trim();
      if (!trimmedValue) {
        this.error = '';
        return;
      }

      // ISBN validation
      if (/^\d+$/.test(trimmedValue)) {
        if (trimmedValue.length !== 10 && trimmedValue.length !== 13) {
          this.error = 'ISBN必须是10位或13位数字';
          return;
        }
      }
      this.error = '';
    },
    handleSearch() {
      const initialInput = this.searchInput.trim();
      if (!initialInput) {
        this.error = '请输入搜索内容';
        return;
      }

      // 清除之前的防抖定时器
      if (this.debounceTimeout) {
        clearTimeout(this.debounceTimeout);
        console.log('已清除之前的防抖定时器');
      }

      // 如果存在进行中的请求，先取消
      if (this.currentRequest) {
        this.currentRequest.cancel('新的搜索请求');
        console.log('已取消之前的搜索请求');
        this.currentRequest = null;
        this.isSearching = false;
      }

      // 确保每次搜索请求都能正确处理
      if (this.isSearching) {
        console.log('当前正在搜索，忽略新的搜索请求');
        return;
      }

      // 设置新的防抖定时器
      this.debounceTimeout = setTimeout(async () => {
        try {
          const currentInput = this.searchInput.trim();
          if (!currentInput) return;

          // 创建新的可取消请求
          const cancelToken = axios.CancelToken.source();
          this.currentRequest = cancelToken;
          this.isSearching = true;
          
          this.$emit('search-start');
          console.log('开始搜索:', currentInput);
          
          // 使用最新输入值发起请求
          await this.$emit('search', currentInput, cancelToken.token);
          
          console.log('搜索成功:', currentInput);
        } catch (error) {
          // 统一处理取消请求的情况
          if (axios.isCancel(error)) {
            console.log('请求取消:', error.message);
            return;
          }
          
          console.error('搜索错误:', error);
          let errorMessage = '搜索请求失败，请重试';
          
          if (error.response) {
            errorMessage = error.response.data.message || '服务器返回错误';
          } else if (error.request) {
            errorMessage = '无法连接到服务器';
          }
          
          // 显示错误但不清空输入
          this.error = `搜索失败: ${errorMessage}`;
          this.$emit('search-error', error);
        } finally {
          // 请求完成后清理
          this.currentRequest = null;
          this.isSearching = false;
          this.$emit('search-end');
          console.log('搜索结束');
        }
      }, 50); // 优化防抖时间
    },
    
    beforeUnmount() {
      // 组件卸载时清理
      if (this.debounceTimeout) {
        clearTimeout(this.debounceTimeout);
      }
      if (this.currentRequest) {
        this.currentRequest.cancel('组件卸载');
      }
    },
  }
};
</script>

<style scoped>
.search-bar {
  max-width: 800px;
  margin: 0 auto;
}

.card {
  border: none;
  background: #fff;
  transition: all 0.3s ease;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15) !important;
}

.btn-primary {
  padding-left: 2rem;
  padding-right: 2rem;
}

.form-control:focus {
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
  border-color: #80bdff;
}
</style>