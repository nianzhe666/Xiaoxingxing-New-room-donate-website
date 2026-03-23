App({
  onLaunch: function () {
    // 初始化小程序
    console.log('小程序启动');
    
    // 获取用户信息
    wx.getSetting({
      success: res => {
        if (res.authSetting['scope.userInfo']) {
          // 已经授权，可以直接调用 getUserInfo 获取头像昵称
          wx.getUserInfo({
            success: res => {
              this.globalData.userInfo = res.userInfo
              // 可以将 res 发送给后台解码出 unionId
              // 由于 getUserInfo 是网络请求，可能会在 Page.onLoad 之后才返回
              // 所以此处加入 callback 以防止这种情况
              if (this.userInfoReadyCallback) {
                this.userInfoReadyCallback(res)
              }
            }
          })
        }
      }
    })
    
    // 获取openid
    this.getOpenid();
  },
  
  getOpenid: function() {
    // 调用登录接口
    wx.login({
      success: res => {
        if (res.code) {
          // 发送 code 到后台换取 openid
          wx.request({
            url: 'https://your-domain.com/api/get_openid',
            data: {
              code: res.code
            },
            success: res => {
              if (res.data.code == 200) {
                this.globalData.openid = res.data.openid;
              }
            }
          });
        } else {
          console.log('登录失败！' + res.errMsg);
        }
      }
    });
  },
  
  globalData: {
    userInfo: null,
    openid: null
  }
})