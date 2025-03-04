<template>
  <div id="app">
    <nav class="navbar navbar-expand-lg navbar-primary bg-primary">
      <div class="container">
        <a class="navbar-brand text-white" href="#">
          <i class="bi bi-book-half"></i> E-Book Search
        </a>
      </div>
    </nav>

    <div class="container pb-5">
      <div class="app-content">
        <SearchBar @search="handleSearch" />
        
        <SearchResults 
          :books="searchResults"
          :platforms="platforms"
          :hasSearched="hasSearched"
        />
      </div>
    </div>
    
    <footer class="app-footer">
      <div class="container">
        <div class="footer-content">
          <div class="footer-logo">
            <i class="bi bi-book-half"></i> E-Book Search
          </div>
          <div class="footer-text">© 2024 E-Book Search. 一站式电子书搜索平台</div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
import SearchBar from './components/SearchBar.vue'
import SearchResults from './components/SearchResults.vue'
import axios from 'axios'

// 根据环境确定API基础URL
const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? window.location.origin + '/api' // 生产环境使用相对路径
  : '/api'; // 开发环境使用代理

export default {
  name: 'App',
  components: {
    SearchBar,
    SearchResults
  },
  data() {
    return {
      searchResults: [],
      platforms: [
        { id: 'zlibrary', name: 'Z-Library', available: true, total: 0 }
      ],
      hasSearched: false
    }
  },
  methods: {
    async handleSearch(keyword) {
      try {
        this.hasSearched = true;
        this.searchResults = []; // 清空之前的搜索结果
        const response = await axios.get(`${API_BASE_URL}/zlibrary/s/${encodeURIComponent(keyword)}`);
        
        if (response.data) {
          this.searchResults = response.data.books;
          
          // 更新平台状态
          if (response.data.platform_status) {
            const status = response.data.platform_status;
            this.platforms = [{
              id: status.id,
              name: status.name,
              available: status.available,
              total: status.total
            }];
          }
        }
      } catch (error) {
        console.error('Search failed:', error);
        this.searchResults = [];
        this.platforms = this.platforms.map(p => ({
          ...p,
          available: false,
          total: 0
        }));
      }
    }
  }
}
</script>

<style>
#app {
  min-height: 100vh;
  background-color: #f8fafc;
  display: flex;
  flex-direction: column;
}

.navbar {
  margin-bottom: 2rem;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  background: linear-gradient(135deg, #4f46e5, #3b82f6) !important;
  padding: 1rem 0;
}

.navbar-brand {
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: #ffffff !important;
  font-size: 1.25rem;
  letter-spacing: 0.5px;
}

.navbar-brand i {
  font-size: 1.5rem;
}

.container {
  max-width: 1200px;
  padding: 0 1.5rem;
  margin: 0 auto;
  width: 100%;
}

.app-content {
  flex: 1;
  padding: 1rem 0 3rem;
}

.app-footer {
  margin-top: auto;
  background-color: #1e293b;
  color: #e2e8f0;
  padding: 2rem 0;
}

.footer-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  text-align: center;
}

.footer-logo {
  font-weight: 600;
  font-size: 1.25rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.footer-text {
  font-size: 0.875rem;
  opacity: 0.8;
}

@media (max-width: 768px) {
  .container {
    padding: 0 1rem;
  }
  
  .navbar {
    padding: 0.75rem 0;
  }
  
  .navbar-brand {
    font-size: 1.125rem;
  }
}
</style>