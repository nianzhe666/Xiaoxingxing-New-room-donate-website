export default {  async fetch(request, env, ctx) {    // 解析请求URL    const url = new URL(request.url);    const path = url.pathname;    
    // 静态文件处理    if (path.startsWith('/static/')) {
      try {
        const filePath = path.substring(1); // 移除开头的斜杠
        const asset = await env.ASSETS.fetch(new Request(`https://${url.hostname}/${filePath}`, request));
        return asset;
      } catch (error) {
        return new Response('Not Found', { status: 404 });
      }
    }
    
    // 对于其他请求，返回静态HTML文件
    if (path === '/' || path === '/index.html') {
      try {
        const asset = await env.ASSETS.fetch(new Request(`https://${url.hostname}/index.html`, request));
        return asset;
      } catch (error) {
        return new Response('Not Found', { status: 404 });
      }
    }
    
    if (path === '/donations' || path === '/donations.html') {
      try {
        const asset = await env.ASSETS.fetch(new Request(`https://${url.hostname}/donations.html`, request));
        return asset;
      } catch (error) {
        return new Response('Not Found', { status: 404 });
      }
    }
    
    // 默认返回index.html
    try {
      const asset = await env.ASSETS.fetch(new Request(`https://${url.hostname}/index.html`, request));
      return asset;
    } catch (error) {
      return new Response('Not Found', { status: 404 });
    }
  },};