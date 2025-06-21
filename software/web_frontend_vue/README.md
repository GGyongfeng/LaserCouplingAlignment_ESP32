# Vue 3 + TypeScript + Vite

一个为自己搭建的易用通用的Vite + Vue + TS的项目框架

## 使用方法

```bash
git clone https://github.com/GGyongfeng/My-Vue-App.git
npm install
npm run dev
```



## 使用技术：

1. element-plus
2. Vite + Vue + TS
3. sass css中的js
4. pinia 变量跨域使用
5. localstore 本机缓存

## 功能&用法：

1. 自动对比版本，用户版本不一致的时候强制刷新，版本为 `VITE_APP_VERSION`

2. 标题为.env里面的`VITE_APP_TITLE`

3. 多环境.env
   执行 `npm run dev` 的时候 使用`.env.development`
   执行 `npm run build` 的时候 使用`.env.production`
   执行 `npm run build：XX` 的时候 就使用`.env.production.XX`

4. src/layouts 布局文件夹：里面有几种常用的响应式布局
   prompt:请帮我在src/layouts里面生成一个XXX（详细描述）样式的布局.vue文件，文件名按照用途或者特点命名，注释说明用处和用法。

5. 更合理的根组件写法：
   app.vue里面仅包含 <router-view>，作为路由视图的容器
   不包含具体的页面内容，只负责路由切换
   更符合"关注点分离"的原则，便于维护和扩展