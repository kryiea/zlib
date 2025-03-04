<template>
  <div class="search-results">
    <!-- 平台状态栏 -->
    <div class="platform-status-bar" v-if="platforms.length > 0">
      <div class="platform-status-title">搜索来源:</div>
      <div class="platform-badges">
        <span v-for="platform in platforms" 
              :key="platform.id"
              :class="['platform-badge', {'platform-badge-available': platform.available}]">
          {{ platform.name }}: {{ platform.available ? `找到 ${platform.total} 个结果` : '无结果' }}
        </span>
      </div>
    </div>

    <!-- 搜索结果表格 -->
    <div class="results-table" v-if="books.length > 0">
      <div class="table-header">
        <div class="col-book-info">
          书籍信息
          <button class="sort-button" @click="toggleSort" :title="getSortTitle">
            年份排序
            <i class="bi" :class="getSortIcon"></i>
          </button>
        </div>
        <div class="col-author">作者</div>
        <div class="col-publisher">出版商</div>
        <div class="col-link">直达链接</div>
        <div class="col-source">来源平台</div>
      </div>

      <div class="table-row" v-for="book in sortedBooks" :key="book.isbn" :class="{'table-row-hover': true}">
        <div class="col-book-info">
          <div class="book-info-main">
            <div class="book-title">{{ book.title }}</div>
            <div class="book-author" v-if="book.author">{{ book.author }}</div>
          </div>
          <div class="book-details">
            <span v-if="book.year" class="book-detail-item"><i class="bi bi-calendar3"></i> {{ book.year }}</span>
            <span v-if="book.language" class="book-detail-item"><i class="bi bi-translate"></i> {{ book.language }}</span>
            <span v-if="book.filesize" class="book-detail-item"><i class="bi bi-file-earmark"></i> {{ book.filesize }}</span>
            <span v-if="book.extension" class="book-detail-item"><i class="bi bi-file-earmark-text"></i> {{ book.extension }}</span>
            <span v-if="book.isbn" class="book-detail-item"><i class="bi bi-upc-scan"></i> ISBN: {{ book.isbn }}</span>
          </div>
        </div>
        <div class="col-author">{{ book.author }}</div>
        <div class="col-publisher">{{ book.publisher }}</div>
        <div class="col-link">
          <a :href="book.book_url" target="_blank" class="download-link">
            <i class="bi bi-download"></i> 下载
          </a>
        </div>
        <div class="col-source">
          <span :class="['source-badge', `source-${book.platform_id}`]">
            {{ book.source }}
          </span>
        </div>
      </div>
    </div>

    <!-- 无结果提示 -->
    <div v-else-if="hasSearched" class="no-results">
      <div class="no-results-content">
        <i class="bi bi-search text-muted mb-3" style="font-size: 3rem;"></i>
        <h4>未找到相关书籍</h4>
        <p class="text-muted">请尝试使用其他关键词搜索</p>
      </div>
    </div>

    <!-- 默认示例书籍 -->
    <div v-else class="example-books">
      <div class="example-title"><i class="bi bi-info-circle me-2"></i>示例书籍</div>
      <div class="results-table">
        <div class="table-header">
          <div class="col-book-info">
            书籍信息
            <button class="sort-button" @click="toggleSort" :title="getSortTitle">
              年份排序
              <i class="bi" :class="getSortIcon"></i>
            </button>
          </div>
          <div class="col-author">作者</div>
          <div class="col-publisher">出版商</div>
          <div class="col-link">直达链接</div>
          <div class="col-source">来源平台</div>
        </div>
        
        <div class="table-row" v-for="book in sortedExampleBooks" :key="book.isbn" :class="{'table-row-hover': true}">
          <div class="col-book-info">
            <div class="book-title">{{ book.title }}</div>
            <div class="book-details">
              <span class="book-detail-item"><i class="bi bi-calendar3"></i> {{ book.year }}</span>
              <span class="book-detail-item"><i class="bi bi-translate"></i> {{ book.language }}</span>
              <span class="book-detail-item"><i class="bi bi-file-earmark"></i> {{ book.filesize }}</span>
              <span class="book-detail-item"><i class="bi bi-file-earmark-text"></i> {{ book.extension }}</span>
            </div>
          </div>
          <div class="col-author">{{ book.author }}</div>
          <div class="col-publisher">{{ book.publisher }}</div>
          <div class="col-link">
            <button class="download-link" disabled>
              <i class="bi bi-download"></i> 示例
            </button>
          </div>
          <div class="col-source">
            <span class="source-badge">{{ book.source }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SearchResults',
  props: {
    books: {
      type: Array,
      default: () => []
    },
    platforms: {
      type: Array,
      default: () => [
        { id: 'zlibrary', name: 'Z-Library', available: true, total: 0 }
      ]
    },
    hasSearched: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      sortOrder: 'desc',  // 默认降序排列
      debounceTimer: null,
      exampleBooks: [
        {
          title: '示例书籍 1',
          author: '作者名称',
          year: '2024',
          pages: '300',
          language: '简体中文',
          filesize: '10 MB',
          extension: 'PDF',
          publisher: '示例出版社',
          source: 'Z-Library',
          platform_id: 'zlibrary'
        },
        {
          title: '示例书籍 2',
          author: '示例作者',
          year: '2023',
          pages: '250',
          language: '英文',
          filesize: '8 MB',
          extension: 'EPUB',
          publisher: 'Example Press',
          source: 'Z-Library',
          platform_id: 'zlibrary'
        }
      ]
    }
  },
  computed: {
    getSortTitle() {
      switch(this.sortOrder) {
        case 'none':
          return '点击降序排列';
        case 'desc':
          return '点击升序排列';
        case 'asc':
          return '点击取消排序';
        default:
          return '默认排序标题'; // 根据需求调整
      }
    },
    getSortIcon() {
      switch(this.sortOrder) {
        case 'none':
          return 'bi-dash';
        case 'desc':
          return 'bi-sort-down';
        case 'asc':
          return 'bi-sort-up';
        default:
          return 'bi-dash';
      }
    },
    sortedBooks() {
      return this.sortBooks(this.books);
    },
    sortedExampleBooks() {
      return this.sortBooks(this.exampleBooks);
    }
  },
  methods: {
    toggleSort() {
      // 循环切换排序状态：none -> desc -> asc
      switch(this.sortOrder) {
        case 'none':
          this.sortOrder = 'desc';
          break;
        case 'desc':
          this.sortOrder = 'asc';
          break;
        case 'asc':
          this.sortOrder = 'none';
          break;
        default:
          this.sortOrder = 'none';
      }
      this.persistSortOrder(this.sortOrder);
    },
    persistSortOrder(order) {
      localStorage.setItem('bookSortOrder', order);
    },
    sortBooks(books) {
      if (this.sortOrder === 'none') {
        return books;
      }
      
      return [...books].sort((a, b) => {
        const yearA = parseInt(a.year, 10) || 0;
        const yearB = parseInt(b.year, 10) || 0;
        
        if (yearA === yearB) {
          return a.title.localeCompare(b.title);
        }
        
        return this.sortOrder === 'asc' ? yearA - yearB : yearB - yearA;
      });
    },
  }
}
</script>

<style scoped>
.search-results {
  margin-top: 20px;
}

.platform-status-bar {
  margin-bottom: 1.5rem;
  padding: 1rem 1.25rem;
  background-color: #ffffff;
  border-radius: 12px;
  display: flex;
  align-items: center;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.platform-status-bar:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0,0,0,0.08);
}

.platform-status-title {
  margin-right: 1rem;
  font-weight: 600;
  color: #374151;
}

.platform-badges {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.platform-badge {
  padding: 0.5rem 1rem;
  border-radius: 8px;
  background-color: #f3f4f6;
  color: #4b5563;
  font-size: 0.875rem;
  font-weight: 500;
  transition: all 0.2s ease;
  box-shadow: 0 1px 2px rgba(0,0,0,0.05);
}

.platform-badge-available {
  background-color: #10b981;
  color: #ffffff;
  box-shadow: 0 2px 4px rgba(16,185,129,0.2);
}

.results-table {
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.results-table:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0,0,0,0.08);
}

.table-header {
  display: grid;
  grid-template-columns: minmax(300px, 3fr) minmax(150px, 1fr) minmax(150px, 1fr) minmax(120px, 1fr) minmax(120px, 1fr);
  gap: 1rem;
  background-color: #f9fafb;
  padding: 1.25rem 1.5rem;
  font-weight: 600;
  color: #374151;
  border-bottom: 1px solid #e5e7eb;
  align-items: center;
  letter-spacing: 0.025em;
}

.table-row {
  display: grid;
  grid-template-columns: minmax(300px, 3fr) minmax(150px, 1fr) minmax(150px, 1fr) minmax(120px, 1fr) minmax(120px, 1fr);
  gap: 1rem;
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid #e5e7eb;
  transition: all 0.2s ease;
  align-items: center;
}

.table-row-hover:hover {
  background-color: #f9fafb;
}

.book-info-main {
  margin-bottom: 0.75rem;
}

.book-title {
  font-weight: 600;
  color: #111827;
  line-height: 1.5;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  white-space: normal;
  min-height: 3em;
  font-size: 1rem;
}

.book-author {
  font-size: 0.875rem;
  color: #4b5563;
  margin-top: 0.375rem;
  font-weight: 500;
}

.book-details {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  font-size: 0.875rem;
  color: #6b7280;
  line-height: 1.5;
}

.book-detail-item {
  display: inline-flex;
  align-items: center;
  white-space: nowrap;
  gap: 0.375rem;
  background-color: #f3f4f6;
  padding: 0.25rem 0.625rem;
  border-radius: 6px;
  transition: all 0.2s ease;
}

.book-detail-item:hover {
  background-color: #e5e7eb;
}

.book-detail-item i {
  font-size: 0.875rem;
  color: #6b7280;
}

.download-link {
  padding: 0.375rem 1rem;
  background-color: #10b981;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  transition: all 0.3s ease;
  min-width: 90px;
  height: 36px;
  font-weight: 500;
  box-shadow: 0 2px 4px rgba(16,185,129,0.2);
}

.download-link:hover {
  background-color: #059669;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(16,185,129,0.3);
}

.download-link:active {
  transform: translateY(0);
}

.download-link:disabled {
  background-color: #e5e7eb;
  color: #9ca3af;
  cursor: not-allowed;
  box-shadow: none;
}

.source-badge {
  padding: 0.375rem 0.75rem;
  border-radius: 6px;
  background-color: #10b981;
  color: white;
  font-size: 0.875rem;
  font-weight: 500;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  height: 36px;
  min-width: 90px;
  box-shadow: 0 2px 4px rgba(16,185,129,0.2);
}

.source-zlibrary {
  background-color: #10b981;
}

.no-results {
  text-align: center;
  padding: 4rem 1.5rem;
  color: #6b7280;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

.no-results-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.example-books {
  opacity: 0.8;
}

.example-title {
  margin-bottom: 1rem;
  font-weight: 500;
  color: #4b5563;
  font-size: 0.875rem;
  display: flex;
  align-items: center;
}

.col-link {
  display: flex;
  align-items: center;
  justify-content: center;
}

.col-source {
  display: flex;
  align-items: center;
  justify-content: center;
}

.sort-button {
  background: none;
  border: none;
  color: #4b5563;
  cursor: pointer;
  padding: 0.25rem 0.5rem;
  margin-left: 0.5rem;
  font-size: 0.875rem;
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  border-radius: 4px;
  transition: all 0.2s ease;
  user-select: none;
}

.sort-button:hover {
  background-color: #e5e7eb;
}

.sort-button .bi {
  font-size: 1rem;
  line-height: 1;
  transition: transform 0.2s ease;
}

.bi-sort-up {
  transform: translateY(-1px);
}

.bi-sort-down {
  transform: translateY(1px);
}   

.bi-dash {
  opacity: 0.5;
}
</style>