<template>
  <div class="search-bar mb-4">
    <div class="card shadow-sm">
      <div class="card-body p-4">
        <div class="search-header mb-4">
          <h3 class="search-title">📚 电子书搜索</h3>
          <p class="search-subtitle">快速找到您需要的电子书资源</p>
        </div>
        <div class="form-group">
          <div class="input-group search-input-group mb-3">
            <span class="input-group-text search-icon">
              <i class="bi bi-search"></i>
            </span>
            <input
              v-model="searchInput"
              type="text"
              class="form-control form-control-lg search-input"
              placeholder="输入书名、作者或ISBN码"
              @keyup.enter="handleSearch"
              autocomplete="off"
            />
            <button
              @click="handleSearch"
              class="btn btn-primary btn-lg search-button"
              :disabled="!isValidInput"
              :class="{'btn-loading': isSearching}"
            >
              <span v-if="!isSearching">搜索</span>
              <span v-else class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
            </button>
          </div>
          <div v-if="error" class="alert alert-danger mt-2 search-error">
            <i class="bi bi-exclamation-triangle-fill me-2"></i>
            {{ error }}
          </div>
          <div class="search-tips">
            <i class="bi bi-info-circle me-1"></i>
            <small class="form-text">支持书名、作者或ISBN码（10位或13位数字）搜索</small>
          </div>
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
  border-radius: 12px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
}

.card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.search-header {
  text-align: center;
}

.search-title {
  font-weight: 700;
  color: #4f46e5;
  margin-bottom: 0.5rem;
  font-size: 1.75rem;
}

.search-subtitle {
  color: #6b7280;
  font-size: 1rem;
  margin-bottom: 0;
}

.search-input-group {
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  border-radius: 10px;
  overflow: hidden;
}

.search-icon {
  background-color: #fff;
  border: none;
  border-right: none;
  color: #6b7280;
  padding-left: 1.25rem;
}

.search-input {
  border: none;
  padding: 0.75rem 1rem;
  font-size: 1rem;
  border-left: none;
  border-radius: 0;
}

.search-input:focus {
  box-shadow: none;
  border-color: transparent;
}

.search-button {
  padding-left: 2rem;
  padding-right: 2rem;
  background: linear-gradient(135deg, #4f46e5, #3b82f6);
  border: none;
  font-weight: 600;
  min-width: 100px;
  transition: all 0.3s ease;
}

.search-button:hover:not(:disabled) {
  background: linear-gradient(135deg, #4338ca, #2563eb);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
}

.search-button:active:not(:disabled) {
  transform: translateY(0);
}

.btn-loading {
  opacity: 0.8;
}

.search-error {
  border-radius: 8px;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
}

.search-tips {
  display: flex;
  align-items: center;
  margin-top: 0.75rem;
  color: #6b7280;
  padding: 0 0.5rem;
}

@media (max-width: 768px) {
  .search-title {
    font-size: 1.5rem;
  }
  
  .search-subtitle {
    font-size: 0.9rem;
  }
  
  .search-button {
    padding-left: 1.5rem;
    padding-right: 1.5rem;
  }
}
</style>