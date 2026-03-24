export default {
  async fetch(request, env, ctx) {
    // 解析请求URL
    const url = new URL(request.url);
    const path = url.pathname;
    
    // 对于静态文件，直接返回
    if (path.startsWith('/static/') || path.includes('.')) {
      return env.ASSETS.fetch(request);
    }
    
    // 对于根路径，返回index.html
    if (path === '/') {
      return env.ASSETS.fetch(new Request(`${url.origin}/index.html`, request));
    }
    
    // 对于其他路径，尝试返回对应的HTML文件
    const htmlPath = `${path}.html`;
    const htmlRequest = new Request(`${url.origin}${htmlPath}`, request);
    const htmlResponse = await env.ASSETS.fetch(htmlRequest);
    
    if (htmlResponse.status === 200) {
      return htmlResponse;
    }
    
    // 如果没有对应的HTML文件，返回index.html
    return env.ASSETS.fetch(new Request(`${url.origin}/index.html`, request));
  },
};