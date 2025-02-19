const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  //transpileDependencies: true,
  devServer: {
    proxy: {
      '/api': {
        target: 'http://localhost:5000',  // 后端服务器地址
        changeOrigin: true,
        pathRewrite: {
          '^/api': ''  // 移除 /api 前缀
        }
      }
    }
  }
}) 