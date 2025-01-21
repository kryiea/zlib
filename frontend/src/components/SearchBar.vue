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
export default {
  name: 'SearchBar',
  data() {
    return {
      searchInput: '',
      error: ''
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
      if (this.isValidInput) {
        this.$emit('search', this.searchInput.trim());
      }
    }
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