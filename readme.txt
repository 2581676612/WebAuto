环境配置：
    1、chromedriver
        打开谷歌浏览器，点击右上角三个点->帮助->关于，查看当前浏览器版本
        打开网址：https://registry.npmmirror.com/binary.html?path=chromedriver/
        找到与上面获取到的版本相同或相近的版本文件夹进入，选择使用环境平台的压缩包下载
        对下载的压缩包解压后，获取到chromedriver文件，替换到Tools目录下
        修改根目录下config.cfg->ChromeDriver->file值为解压的文件。注意：文件后缀名也要写上
    2、geckodriver（火狐浏览器driver-辅助测试使用（邀请、会议相关））
        查看当前设备火狐浏览器版本号
        打开网址：https://registry.npmmirror.com/binary.html?path=geckodriver/
        后续操作同chromedriver
    3、自动化脚本环境配置
        python版本-3.7.5（其他版本可能三方库不兼容）
        pip install -r requirements.txt  安装环境依赖
    4、mac系统给pycharm添加权限控制pc（上传文件需要自动化控制文件夹）
        系统偏好设置->安全性与隐私,辅助功能勾选上pycharm

框架结构：
    core--自动化脚本
        base--基础功能
            base_case--用例基类（可配置所有用例执行前后的操作）
            common--通用方法
            cv--图像识别相关脚本
            logger--日志模块
            parse--解析配置文件参数
            report--测试报告配置
            setting--用例执行方法
        browser--浏览器对象
            chrome--google浏览器对象
            firefox--火狐浏览器对象
        modules--阅流网站模块
            control--模块间通用脚本
            project--项目模块脚本
            shoot--拍摄模块脚本
    report--测试报告
    scripts--测试用例
        case--回归用例
            project--项目相关用例
            shoot--拍摄相关用例
        loopcase--压测用例
        setup--前置操作（登录）
        teardown--后置操作（关闭浏览器）
    statics--静态文件
        downloads--存储下载文件（下载后删除，只为了检测下载文件数是否正确）
        img_demo--存储图片模版（部分弹窗无法使用selenium点击，使用opencv图像识别点击）
        tools--自动化相关工具（浏览器driver）
        upload_file--上传用例使用文件
    config.cfg--配置文件
    conftest.py--pytest配置脚本
    main.py--执行用例脚本
    pytest.ini--pytest配置参数
    requirements.txt--环境依赖三方库
    project_case.txt--项目模块用例集
    shoot_case.txt--拍摄模块用例集

配置文件--config.cfg：
    Environment->web_type: 自动化测试网站（None-执行生产环境；测试环境、体验环境修改值为sit几、uat几）
    UserInfo: 登录用户账号信息（1为主测试账号，2、3为辅助测试使用）
    TestCase：测试用例
    Project->name: 创建的测试项目名称
    Project->camera: 创建的测试机位名称
    Project->copy_camera: 创建的辅助测试机位名称
    Report->test_people: 测试用例执行人（报告上显示）
    loop->count: 压测次数

用例执行：
    修改根目录下config.cfg->TestCase->case值为待测用例
    可直接指定测试用例，用例路径从AutoTest下级开始。例：case/test_登录.py
    也可使用txt文件执行用例集，用例执行顺序为从上到下
    配置文件配置完成，执行根目录下main.py文件

注意事项：
    1、建议关闭浏览器自动更新设置，更新后，当前driver可能无法兼容
    2、web自动化用例依赖登录，功能用例需在登录状态下执行，且用例最后需带上case/teardown/test_close.py关闭模拟浏览器
    3、自动化启动后，请勿操作当前PC。部分弹窗需浏览器显示在最前面才能检测到。上传文件需设备聚焦在当前浏览器。执行期间操作pc可能影响到用例执行
