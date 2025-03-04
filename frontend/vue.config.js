const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  //transpileDependencies: true,
  devServer: {
    proxy: {
      '/api': {
        target: process.env.NODE_ENV === 'production' ? 'http://8.138.107.27:5000' : 'http://localhost:5000',  // 后端服务器地址
        changeOrigin: true,
        pathRewrite: {
          '^/api': ''  // 移除 /api 前缀
        }
      }
    }
  },
  // 确保生产环境构建正确处理路径
  publicPath: process.env.NODE_ENV === 'production' ? '/' : '/'
})