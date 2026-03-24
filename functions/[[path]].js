export default {
  async fetch(request, env, ctx) {
    // 解析请求URL
    const url = new URL(request.url);
    const path = url.pathname;
    
    // 对于根路径，返回index.html
    if (path === '/') {
      return env.ASSETS.fetch(new Request(`${url.origin}/index.html`, request));
    }
    
    // 对于其他路径，直接返回对应的文件
    return env.ASSETS.fetch(request);
  },
};