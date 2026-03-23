const app = getApp();

Page({
  data: {
    item: null,
    contact: {},
    showContactModal: false
  },
  
  onLoad: function (options) {
    const itemId = options.id;
    this.getItemDetail(itemId);
    this.getContact();
  },
  
  getItemDetail: function (itemId) {
    wx.showLoading({
      title: '加载中...'
    });
    
    // 使用缓存减少网络请求
    const cachedItem = wx.getStorageSync(`item_${itemId}`);
    const cacheTime = wx.getStorageSync(`item_${itemId}_cache_time`);
    
    // 如果缓存存在且未过期（5分钟）
    if (cachedItem && cacheTime && (Date.now() - cacheTime) < 5 * 60 * 1000) {
      this.setData({
        item: cachedItem
      });
      wx.hideLoading();
      return;
    }
    
    wx.request({
      url: `https://your-domain.com/api/item/${itemId}`,
      method: 'GET',
      // 启用缓存
      header: {
        'Cache-Control': 'max-age=300'
      },
      success: res => {
        if (res.data.code == 200) {
          const item = res.data.data;
          this.setData({
            item: item
          });
          
          // 缓存数据
          wx.setStorageSync(`item_${itemId}`, item);
          wx.setStorageSync(`item_${itemId}_cache_time`, Date.now());
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
  },
  
  getContact: function () {
    // 使用缓存减少网络请求
    const cachedContact = wx.getStorageSync('contact');
    const cacheTime = wx.getStorageSync('contact_cache_time');
    
    // 如果缓存存在且未过期（30分钟）
    if (cachedContact && cacheTime && (Date.now() - cacheTime) < 30 * 60 * 1000) {
      this.setData({
        contact: cachedContact
      });
      return;
    }
    
    wx.request({
      url: 'https://your-domain.com/api/contact',
      method: 'GET',
      // 启用缓存
      header: {
        'Cache-Control': 'max-age=1800'
      },
      success: res => {
        if (res.data.code == 200) {
          const contact = res.data.data;
          this.setData({
            contact: contact
          });
          
          // 缓存数据
          wx.setStorageSync('contact', contact);
          wx.setStorageSync('contact_cache_time', Date.now());
        }
      }
    });
  },
  
  wechatPay: function () {
    const itemId = this.data.item.id;
    const openid = app.globalData.openid;
    
    if (!openid) {
      wx.showToast({
        title: '获取用户信息失败，请重试',
        icon: 'none'
      });
      return;
    }
    
    wx.showLoading({
      title: '准备支付...'
    });
    
    wx.request({
      url: 'https://your-domain.com/api/create_payment',
      method: 'POST',
      data: {
        item_id: itemId,
        openid: openid
      },
      success: res => {
        if (res.data.code == 200) {
          const prepayId = res.data.data.prepay_id;
          if (prepayId) {
            // 调用微信支付
            wx.requestPayment({
              timeStamp: res.data.data.timeStamp,
              nonceStr: res.data.data.nonceStr,
              package: `prepay_id=${prepayId}`,
              signType: 'RSA',
              paySign: res.data.data.paySign,
              success: () => {
                wx.showToast({
                  title: '支付成功',
                  icon: 'success'
                });
                // 清除缓存，强制刷新
                wx.removeStorageSync(`item_${itemId}`);
                wx.removeStorageSync(`item_${itemId}_cache_time`);
                // 刷新页面
                this.getItemDetail(itemId);
              },
              fail: () => {
                wx.showToast({
                  title: '支付失败',
                  icon: 'none'
                });
              },
              complete: () => {
                wx.hideLoading();
              }
            });
          } else {
            wx.showToast({
              title: '创建支付订单失败',
              icon: 'none'
            });
          }
        } else {
          wx.showToast({
            title: res.data.message,
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
  },
  
  showContact: function () {
    this.setData({
      showContactModal: true
    });
  },
  
  closeContact: function () {
    this.setData({
      showContactModal: false
    });
  }
})