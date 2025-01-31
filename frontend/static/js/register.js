document.getElementById("register-form").addEventListener("submit", function(e) {
    e.preventDefault();  // 阻止表单的默认提交行为

    const username = document.getElementById("username").value;
    const email = document.getElementById("email").value;
    const phone = document.getElementById("phone").value;
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirm_password").value;


    // 邮箱格式验证
    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    if (!emailRegex.test(email)) {
        alert("请输入有效的邮箱地址！");
        return;  // 如果邮箱格式不正确，终止表单提交
    }

    // 手机号格式验证（中国大陆手机号）
    const phoneRegex = /^1\d{10}$/;
    if (!phoneRegex.test(phone)) {
        alert("请输入有效的手机号！");
        return;  // 如果手机号格式不正确，终止表单提交
    }
        
    // 表单验证：检查密码和确认密码是否匹配
    if (password !== confirmPassword) {
        alert("密码和确认密码不匹配！");
        return;  // 如果不匹配，终止表单提交
    }

    // 创建一个包含用户输入数据的对象
    const data = {
        username: username,
        email: email,
        phone: phone,
        password: password,
        confirm_password: confirmPassword
    };

    // 使用 Fetch API 向服务器发送注册请求
    fetch('/api/register', {
        method: 'POST',  // 使用 POST 方法提交数据
        headers: {
            'Content-Type': 'application/json'  // 发送的数据格式为 JSON
        },
        body: JSON.stringify(data)  // 将数据转换为 JSON 字符串
    })
    .then(response => response.json())  // 解析服务器返回的 JSON 数据
    .then(data => {
        if (data.message) {
            alert(data.message);  // 如果服务器返回消息，则提示
            window.location.href = '/login';  // 注册成功后跳转到登录页面
        } else {
            alert(data.error);  // 如果有错误，提示错误信息
        }
    })
    .catch(error => console.error('Error:', error));  // 捕获任何错误并输出到控制台
});
