<template>
  <div id="app">
    <nav class="navbar navbar-expand-lg navbar-primary bg-primary">
      <div class="container">
        <a class="navbar-brand text-white" href="#">
          <i class="bi bi-book"></i> E-Book
        </a>
      </div>
    </nav>

    <div class="container pb-5">
      <SearchBar @search="handleSearch" />
      
      <SearchResults 
        :books="searchResults"
        :platforms="platforms"
        :hasSearched="hasSearched"
      />
    </div>
  </div>
</template>

<script>
import SearchBar from './components/SearchBar.vue'
import SearchResults from './components/SearchResults.vue'
import axios from 'axios'

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
        const response = await axios.get(`/api/zlibrary/s/${encodeURIComponent(keyword)}`);
        
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
  background-color: #f3f4f6;
}

.navbar {
  margin-bottom: 2rem;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  background: linear-gradient(to right, #3b82f6, #2563eb) !important;
}

.navbar-brand {
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #ffffff !important;
}

.navbar-brand i {
  font-size: 1.25rem;
}

.container {
  max-width: 1200px;
  padding: 0 1rem;
  margin: 0 auto;
}

@media (max-width: 768px) {
  .container {
    padding: 0 0.75rem;
  }
}
</style>