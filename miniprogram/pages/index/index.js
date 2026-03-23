Page({
  data: {
    items: []
  },
  
  onLoad: function () {
    // 页面加载时获取数据
    this.getItems();
  },
  
  onShow: function () {
    // 页面显示时刷新数据
    this.getItems();
  },
  
  getItems: function () {
    wx.showLoading({
      title: '加载中...'
    });
    
    // 使用缓存减少网络请求
    const cachedItems = wx.getStorageSync('items');
    const cacheTime = wx.getStorageSync('items_cache_time');
    
    // 如果缓存存在且未过期（5分钟）
    if (cachedItems && cacheTime && (Date.now() - cacheTime) < 5 * 60 * 1000) {
      this.setData({
        items: cachedItems
      });
      wx.hideLoading();
      return;
    }
    
    wx.request({
      url: 'https://your-domain.com/api/items',
      method: 'GET',
      // 启用缓存
      header: {
        'Cache-Control': 'max-age=300'
      },
      success: res => {
        if (res.data.code == 200) {
          const items = res.data.data;
          this.setData({
            items: items
          });
          
          // 缓存数据
          wx.setStorageSync('items', items);
          wx.setStorageSync('items_cache_time', Date.now());
        } else {
          wx.showToast({
            title: '获取数据失败',
            icon: 'none'
          });
        }
      },
      fail: err => {
        wx.showToast({
          title: '网络错误',
          icon: 'none'
        });
      },
      complete: () => {
        wx.hideLoading();
      }
    });
  }
})