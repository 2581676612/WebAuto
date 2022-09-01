import re
import pyautogui
import pytest
import screeninfo
import time

from core.base import parse
from core.base.logger import logger
from core.modules.control import Control


class Shoot(Control):
    def enter_shoot_page(self):
        """进入拍摄首页"""
        url = self.url + 'shoot'
        self.open_page(url)
        if self.first_enter_shoot:
            self.first_enter_shoot = False
            self.close_update_info()
            self.close_message()

    def check_input_len(self, input_len=0, default_len=20):
        p_name_count = f'{input_len}/{default_len}'
        logger.info(f'输入字符数为：{p_name_count}')
        current_count = self.get_text(self.find_by_condition('xpath', '//input[@class="item-name-input"]/../span'))
        logger.info(f'实际字符数为：{current_count}')
        if current_count == p_name_count:
            logger.info('字符数检测成功')
        else:
            logger.error('字符数检测失败')
            assert 0

    def create_project(self, p_name=parse.project_name):
        """创建项目（只填写文件名）"""
        if p_name in self.get_my_project_list():
            pytest.skip('该项目已存在，无需创建')
        self.click_by_condition('class', 'iconjiahao_jiahao', '左上角加号图标', 3)
        logger.info('输入项目名称')
        self.find_by_condition('class', 'item-name-input').send_keys(p_name)
        time.sleep(1)
        # 检测输入字符统计
        self.check_input_len(input_len=len(p_name))
        # 点击完成创建
        self.click_by_text('div', '创建 ', False)
        # 等待检测到创建项目成功提示
        if self.wait_until_xpath('//p[contains(text(), "创建项目成功")]'):
            logger.info('检测到提示--创建项目成功')
            time.sleep(3)
        else:
            logger.error('未检测到项目创建成功提示！')
            assert 0

    def create_project_exist(self):
        """拍摄项目重名检测"""
        my_project_list = self.get_my_project_list()
        if not my_project_list:
            pytest.skip('无拍摄项目，跳过用例')
        p_name = my_project_list[0]
        self.click_by_condition('class', 'iconjiahao_jiahao', '左上角加号图标', 3)
        logger.info('输入项目名称')
        self.find_by_condition('class', 'item-name-input').send_keys(p_name)
        time.sleep(1)
        # 点击完成创建
        self.click_by_text('div', '创建 ', False)
        # 等待检测到创建项目成功提示
        if self.wait_until_xpath('//p[contains(text(), "项目名称重复")]'):
            logger.info('检测到提示--项目名称重复')
            self.click_by_condition('class', 'cancel', '取消')
            time.sleep(3)
        else:
            logger.error('未检测到项目名称重复提示！')
            assert 0

    def get_my_project_list(self):
        # 获取我的项目列表
        project_ele_list = self.finds_by_condition('xpath',
                                                   '//div[@class="shoot-list__wrapper"][1]/div/span[@class="title text-overflow"]')
        project_list = [e.get_attribute('innerText') for e in project_ele_list]
        logger.info(f'我的拍摄项目列表为：{project_list}')
        return project_list

    def get_join_project_name_list(self):
        """获取加入项目列表"""
        project_ele_list = self.finds_by_condition('xpath',
                                                   '//div[@class="shoot-list__wrapper"][2]/div/span[@class="title text-overflow"]')
        project_list = [e.get_attribute('innerText') for e in project_ele_list]
        logger.info(f'参与拍摄项目列表为：{project_list}')
        return project_list

    def delete_project(self, project=parse.project_name):
        """删除项目"""
        logger.info('检测是否存在创建的测试项目')
        project_list = self.get_my_project_list()  # 获取项目列表
        while project in project_list:  # 列表内存在测试项目，则删除
            project_ele_list = self.finds_by_condition('xpath',
                                                       '//div[@class="shoot-list__wrapper"][1]/div/span[@class="title text-overflow"]')
            project_count = len(project_ele_list)
            logger.info(f'项目总数为：{project_count}')
            index = 1
            for ele in project_ele_list:
                p_name = ele.get_attribute('innerText')
                if p_name == project:
                    logger.info('检测到创建测试项目')
                    self.click_by_condition('xpath',
                                            f'//div[@class="shoot-list__wrapper"][1]/div[{index}]/span[2]', '更多设置')
                    logger.info('点击--删除项目')
                    self.click_by_text('li', '删除项目')
                    self.click_by_condition('xpath', '//*[@class="space-round"]/div[2]/div[contains(text(), "删除")]',
                                            '删除', 0)
                    self.wait_until_text(text='删除项目成功')
                    self.refresh()
                    project_count -= 1
                    cur_project_count = len(self.get_my_project_list())
                    logger.info(f'当前项目数为：{cur_project_count}')
                    if cur_project_count == project_count:
                        logger.info('删除成功')
                        self.refresh(3)
                        break
                    else:
                        logger.error('删除失败')
                        assert 0
                index += 1
            project_list = self.get_my_project_list()

    def open_project(self, p_name=parse.project_name):
        """点击项目名，打开项目"""
        setting_ele = self.finds_by_condition('xpath',
                                              f'//div[@class="shoot-list__wrapper"][1]//span[contains(text(), "{p_name}")]')
        if len(setting_ele) >= 1:
            logger.info('检测到测试项目')
            setting_ele[0].click()
            time.sleep(3)
        else:
            logger.error('未找到测试项目，请检查项目是否存在！')
            assert 0

    def open_join_project(self, p_name=parse.project_name):
        """点击项目名，打开项目"""
        setting_ele = self.finds_by_condition('xpath',
                                              f'//div[@class="shoot-list__wrapper"][2]//span[contains(text(), "{p_name}")]')
        if len(setting_ele) >= 1:
            logger.info('检测到加入项目')
            setting_ele[0].click()
            time.sleep(3)
        else:
            logger.error('未找到加入项目，请检查项目是否存在！')
            assert 0

    def open_project_menu(self, p_name=parse.project_name):
        """打开项目菜单栏"""
        self.open_project()
        self.click_by_condition('xpath',
                                f'//div[@class="shoot-list__wrapper"][1]//span[contains(text(), "{p_name}")]/../span[2]')

    def open_project_settings(self, setting='拍摄设置', timeout=2):
        """打开项目设置"""
        self.click_by_condition('xpath', f'//li[contains(text(), "{setting}")]', setting, timeout)

    def copy_invite_link(self, role='审阅者'):
        """复制邀请链接"""
        role_ele = self.find_by_condition('class', 'invite-role')  # 获取当前角色元素对象
        current_role = self.get_text(role_ele)  # 获取当前角色值
        logger.info(f'当前邀请角色为：{role}')
        if current_role != role:  # 修改角色
            logger.info('切换邀请角色')
            role_ele.click()
            time.sleep(2)
            self.click_by_text('div', role)
            time.sleep(3)
            if self.get_text(role_ele) == role:
                logger.info('邀请角色切换成功')
            else:
                logger.error('邀请角色切换失败')
                assert 0
        self.click_by_text('span', '复制链接')
        if self.wait_until_xpath('//p[contains(text(), "复制链接成功")]'):
            logger.info('复制链接成功')
            url = self.find_by_condition('xpath', '//div[@class="invite-link"]/span').get_attribute('innerText').strip()
            logger.info(url)
            self.close_invite_view()
            return url

    def close_invite_view(self):
        """关闭邀请对话框"""
        self.click_by_condition_index('xpath', '//div[@class="dialog-header-content"]/i', -1, '关闭邀请界面')

    def accept_invite(self, url):
        """点击链接，加入拍摄项目
            url--邀请链接
        """
        self.open_page(url)  # 打开邀请链接
        self.refresh()  # 刷新页面
        if self.check_condition('xpath', '//div[contains(text(), "进入拍摄项目")]'):  # 显示进入项目，表示已加入
            logger.info('你已在项目内')
            self.click_by_condition('xpath', '//div[contains(text(), "进入拍摄项目")]')  # 点击进入项目
            time.sleep(5)
            for i in range(4):  # 跳过拍摄新手引导
                if self.check_condition('class', 'skip-btn'):
                    self.click_by_condition('class', 'skip-btn')
                    break
                time.sleep(3)
        elif self.check_condition('xpath', '//div[contains(text(), "加入拍摄项目")]'):
            self.click_by_condition('xpath', '//div[contains(text(), "加入拍摄项目")]')  # 点击加入拍摄项目
            time.sleep(3)
            for i in range(4):  # 跳过新手引导
                if self.check_condition('class', 'skip-btn'):
                    self.click_by_condition('class', 'skip-btn')
                    break
                time.sleep(3)
        else:
            logger.error('界面异常')
            assert 0

    def check_join(self):
        """检测加入是否成功"""
        self.refresh()
        join_pro_list = self.get_join_project_name_list()  # 获取加入项目列表
        if parse.project_name in join_pro_list:
            logger.info('参与项目检测到测试项目，加入成功')
            return True
        logger.info('参与项目未检测到测试项目')
        return False

    def check_invite(self):
        """检测邀请是否成功"""
        if self.check_join():
            return True
        logger.error('邀请失败')
        assert 0

    def change_role(self, member='', change_role=''):
        """修改成员角色身份"""
        if not member:  # 检测是否传参
            logger.error('未检测到用户参数!')
            assert 0
        member_ele_list = self.finds_by_condition('class', 'popWin-list-wrapper')  # 获取成员元素列表
        for i in range(1, len(member_ele_list)):
            # 遍历检测成员
            cur_member = self.find_by_condition('xpath',
                                                f'//div[@class="popWin-list-wrapper"][{i + 1}]/div[1]/span[1]'). \
                get_attribute('innerText').strip()
            if cur_member == member:  # 当前成员是要修改的成员
                # 判断当前角色，是管理者就修改为审阅者，审阅者修改为管理者
                cur_role = self.find_by_condition('xpath',
                                                  f'//div[@class="popWin-list-wrapper"][{i + 1}]//span[@class="popWin-text"]'). \
                    get_attribute('innerText').strip()
                if not change_role:
                    change_role = '审阅者' if cur_role == '管理者' else '管理者'
                # 点击成员设置
                self.click_by_condition('xpath',
                                        f'//div[@class="popWin-list-wrapper"][{i + 1}]//span[@class="popWin-text"]/span',
                                        '设置')
                # 点击要修改的身份
                self.click_by_condition_index('xpath', f'//div[contains(text(), "{change_role}")]', -1,
                                              f'{change_role}')
                # 等待操作成功toast提示
                if self.find_by_condition('xpath',
                                          f'//div[@class="popWin-list-wrapper"][{i + 1}]//span[@class="popWin-text"]'). \
                        get_attribute('innerText').strip() == change_role:
                    logger.info(f'修改成员-{member} 角色成功：{cur_role}->{change_role}')
                    time.sleep(3)
                    break
        else:
            logger.info('未检测到该成员！')
            self.close_member_setting_view()  # 关闭成员管理面板
            assert 0
        self.close_member_setting_view()  # 关闭成员管理面板

    def close_member_setting_view(self):
        """关闭成员管理界面"""
        self.click_by_condition('xpath', '//div[@class="role-title"]/i', '关闭成员管理界面')

    def remove_member(self, member=''):
        """删除用户"""
        if not member:  # 未传参，删除所有用户
            logger.info('未检测到用户参数，默认删除所有用户')
        member_ele_list = self.finds_by_condition('class', 'popWin-list-wrapper')  # 获取成员元素列表
        while len(member_ele_list) > 1:  # 成员数大于1，就一直检测
            for i in range(1, len(member_ele_list)):  # 遍历成员列表（删除成员后，列表会变动，需删除后重新获取）
                cur_member = self.find_by_condition('xpath',
                                                    f'//div[@class="popWin-list-wrapper"][{i + 1}]/div[1]/span[1]').get_attribute(
                    'innerText').strip()
                # 未传入用户名，每个用户都删除；传入用户名，删除指定用户
                if (not member) or (member and cur_member == member):
                    self.click_by_condition('xpath',
                                            f'//div[@class="popWin-list-wrapper"][{i + 1}]//span[@class="popWin-text"]/span',
                                            '设置')
                    self.click_by_condition_index('xpath', '//div[contains(text(), "移除成员")]', -1, '移除成员')
                    self.click_by_condition('xpath', '//div[contains(text(), "移除 ")]', '移除')
                    if self.wait_until_xpath('//p[contains(text(), "移除成员成功")]'):
                        logger.info('移除成员成功')
                        time.sleep(3)
                        # 如果传入用户名，删除后则终止循环
                        if member:
                            self.close_member_setting_view()
                            return True
                        break
            else:
                logger.info('未检测到用户！')
                assert 0
            member_ele_list = self.finds_by_condition('class', 'infinite-list-item')
        else:
            logger.info('项目内成员为1，无法删除')
        self.close_member_setting_view()  # 关闭成员面板

    def set_fangluping(self, open=True):
        """设置防录屏"""
        fangluping_ele = self.find_by_condition('xpath',
                                                '//div[@class="record-set-wrap"]/div[@class="switch-wrap"]/div')
        if open:
            if fangluping_ele.get_attribute('aria-checked'):
                logger.info('防录屏开关为打开状态')
                self.close_project_setting()
            else:
                logger.info('防录屏开关未打开，点击打开')
                fangluping_ele.click()
                time.sleep(2)
                self.click_by_text('div', '保存设置')
                self.wait_until_text(text='保存成功')
        else:
            if fangluping_ele.get_attribute('aria-checked'):
                logger.info('防录屏开关为打开状态，点击关闭')
                fangluping_ele.click()
                time.sleep(2)
                self.click_by_text('div', '保存设置')
                self.wait_until_text(text='保存成功')
            else:
                logger.info('防录屏开关为未打开状态')
                self.close_project_setting()

    def check_fangluping(self, open=True):
        """检测防录屏
            open--防录屏状态True/False
        """
        if open:
            if self.check_condition('class', 'iconic_fangluping'):
                logger.info('检测到防录屏标志')
                return True
            else:
                logger.error('未检测到防录屏标志')
                assert 0
        else:
            if self.check_condition('class', 'iconic_fangluping'):
                logger.error('检测到防录屏标志')
                assert 0
            else:
                logger.info('未检测到防录屏标志')
                return True

    def close_project_setting(self):
        """关闭项目设置"""
        self.click_by_condition('xpath', '//div[@class="dialog-header-content"]/i', '关闭项目设置')

    def get_camera_name_list(self):
        """获取机位列表"""
        camera_list = self.finds_by_condition('class', 'camera-name-text')
        camera_name_list = [self.get_text(e) for e in camera_list]
        return camera_name_list

    def create_camera(self, camera_name=parse.camera):
        """创建机位"""
        self.find_by_condition('class', 'item-name-input').send_keys(camera_name)
        time.sleep(1)
        self.check_input_len(input_len=len(camera_name))
        self.click_by_text('div', '完成创建')
        if self.wait_until_text(text='创建机位成功'):
            logger.info('创建成功')
            time.sleep(3)
        else:
            logger.info('创建失败')
            assert 0

    def remove_camera(self, camera=''):
        """删除机位"""
        while camera in self.get_camera_name_list():
            self.open_camera_setting(camera)
            self.click_by_condition('class', 'cancel', '删除机位')
            self.click_by_condition('class', 'delete', '删除')
            if self.wait_until_text(text='删除机位成功'):
                logger.info('删除成功')
                time.sleep(5)
        else:
            logger.info('无同名机位')

    def open_camera_setting(self, camera=''):
        """打开机位配置"""
        camera_list = self.finds_by_condition('class', 'camera-name-text')
        camera_name_list = [self.get_text(e) for e in camera_list]
        for index, ca in enumerate(camera_name_list):
            if ca == camera:
                logger.info(f'检测到机位： {camera}')
                self.click_by_condition_index('class', 'flv-btn-wrapper', index, '机位配置', 5)
                break
        else:
            logger.error(f'未检测到机位：{camera}')
            assert 0

    def open_camera_detail(self, camera=parse.camera):
        """打开机位详情页"""
        camera_list = self.finds_by_condition('class', 'camera-name-text')
        camera_name_list = [self.get_text(e) for e in camera_list]
        for index, ca in enumerate(camera_name_list):
            if ca == camera:
                logger.info(f'检测到机位： {camera}')
                self.click_by_condition_index('class', 'check-btn', index, '监看/回放', 5)
                break
        else:
            logger.error(f'未检测到机位：{camera}')
            assert 0

    def upload_file(self, camera='', file='', select_all=False):
        """上传文件"""
        for i in range(5):
            self.open_camera_setting(camera)
            self.click_by_text('div', '拍摄素材回放')
            self.click_by_condition('class', 'shoot__upload', '上传文件', 3)
            self.choose_file_to_upload(file, select_all)
            self.open_upload_page()
            if self.is_file_upload():
                break
            logger.info('文件未正确选取，重试！')

    def upload_dir(self, camera=''):
        """上传文件夹"""
        for i in range(5):
            self.open_camera_setting(camera)
            self.click_by_text('div', '拍摄素材回放')
            self.click_by_condition('xpath', '//div[@class="upload-wrap"]/div[2]', '上传文件夹', 3)
            self.choose_file_to_upload()
            time.sleep(3)
            self.click_upload_img()
            self.open_upload_page()
            if self.is_file_upload():
                break
            logger.info('文件未正确选取，重试！')

    def check_advertisement(self, status='open'):
        """检测广告位状态 open/close"""
        if self.check_condition('class', 'ad-wrap'):
            if status == 'open':
                logger.info('检测到广告位')
            else:
                logger.error('检测到广告位')
                assert 0
        else:
            if status == 'close':
                logger.info('未检测到广告位')
            else:
                logger.error('未检测到广告位')
                assert 0

    def close_advertisement(self):
        """关闭广告位"""
        self.click_by_condition('xpath', '//div[@class="ad-wrap"]//span', '关闭广告位')

    def push_by_rtmp(self):
        """rtmp推流"""
        self.click_by_text('div', '实时画面推流')
        self.click_by_text('div', 'RTMP推流')
        content_ele_list = self.finds_by_condition('class', 'live-set-popwin-url')
        push_address, password = self.get_text(content_ele_list[0]), self.get_text(content_ele_list[1])
        copy_ele_list = self.finds_by_condition('class', 'live-set__copy')
        copy_ele_list[0].click()
        self.wait_until_text(text='复制地址成功')
        copy_text = self.get_copy_text()
        logger.info(f'复制结果为：{copy_text}')
        if copy_text[:4] == 'rtmp' and copy_text == push_address:
            logger.info('复制地址成功')
        else:
            logger.error(f'复制地址失败-{copy_text}')
            assert 0
        copy_ele_list[1].click()
        self.wait_until_text(text='复制地址成功')
        copy_text = self.get_copy_text()
        logger.info(f'复制结果为：{copy_text}')
        if copy_text == password:
            logger.info('复制密钥成功')
        else:
            logger.error(f'复制密钥失败-{copy_text}')
            assert 0

    def push_by_srt(self):
        """srt推流"""
        self.click_by_text('div', '实时画面推流')
        self.click_by_text('div', 'SRT推流')
        content_ele = self.find_by_condition('class', 'live-set-popwin-url')
        push_address = self.get_text(content_ele)
        copy_ele = self.find_by_condition('class', 'live-set__copy')
        copy_ele.click()
        self.wait_until_text(text='复制地址成功')
        copy_text = self.get_copy_text()
        logger.info(f'复制结果为：{copy_text}')
        if copy_text[:3] == 'srt' and copy_text == push_address:
            logger.info('复制地址成功')
        else:
            logger.error(f'复制地址失败-{copy_text}')
            assert 0

    def close_camera_setting(self):
        """关闭机位设置"""
        self.click_by_condition('class', 'iconquxiao_quxiao', '关闭机位设置')

    def create_ftp_link(self):
        """生成FTP链接"""
        self.click_by_text(text='拍摄素材回放')
        self.click_by_text(text='生成 FTP 链接')
        host_ele = self.find_by_condition('xpath', '//span[text()="host"]/../div')
        user_ele = self.find_by_condition('xpath', '//span[text()="用户名"]/../div')
        password_ele = self.find_by_condition('xpath', '//span[text()="密码"]/../div')
        host, user, password = self.get_text(host_ele), self.get_text(user_ele), self.get_text(password_ele)
        link_str = f'{host}(用户名：{user}密码：{password})'
        logger.info(link_str)
        if host == 'f.yueliu.cn' and user and password:
            logger.info('host、用户名、密码检测成功')
        self.click_by_condition('class', 'copy', '复制FTP链接地址')
        copy_text = self.get_copy_text()
        if copy_text == link_str:
            logger.info('复制FTP地址成功')
        else:
            logger.error(f'复制FTP地址失败-{copy_text}')

    def open_member_view_by_icon(self):
        """点击头像，打开成员管理"""
        self.click_by_condition('class', 'shoot-member-list-wrapper', '成员头像')
        if self.check_condition('class', 'dialog-header'):
            logger.info('检测到对话框，打开成员管理成功')
            self.close_member_setting_view()
        else:
            logger.error('打开成员管理失败')
            assert 0

    def create_meeting(self):
        """创建会议"""
        self.click_by_condition('class', 'no-meeting', '创建会议')
        self.click_by_img('chrome_allow_voice', '录音权限弹窗')
        time_ele = self.find_by_condition('class', 'meeting-during-time')
        cur_time = time.time()
        while time.time() - cur_time < 30:
            if "准备中" in self.get_text(time_ele):
                logger.info('会议准备中。。。')
                time.sleep(5)
                continue
            elif ":" in self.get_text(time_ele):
                logger.info('会议创建成功')
                break
        else:
            logger.error('会议创建超时，创建失败')
            assert 0

    def leave_meeting(self):
        """离开会议"""
        self.open_meeting_dialog()
        self.click_by_condition('class', 'leave-host', '离开')
        self.click_by_text('div', '离开会议', False)
        self.wait_until_text(text='您已离开语音会议')

    def close_meeting(self):
        """全员结束会议"""
        self.open_meeting_dialog()
        self.click_by_condition('class', 'leave-host', '离开')
        self.click_by_text('div', '全员结束会议', False)
        self.click_by_condition('xpath', '//div[@class="el-message-box__btns"]/button[2]', '结束')
        self.wait_until_text(text='您已离开语音会议')
        self.wait_until_text(text='会议已结束')

    def create_meeting_link(self):
        """创建会议链接"""
        self.click_meeting_icon()
        self.click_by_condition('class', 'voice-setting', '邀请入会', 5)
        link_ele = self.find_by_condition('xpath', '//div[@class="invite-link"]/span')
        invite_link = self.get_text(link_ele)
        self.click_by_text('span', '复制链接')
        if invite_link in self.get_copy_text():
            logger.info('复制链接成功')
            self.close_invite_view()
            return invite_link
        logger.error('复制链接失败')
        self.close_invite_view()
        assert 0

    def check_meeting_dialog(self):
        """检测会议对话框是否打开"""
        if self.check_condition('class', 'heightAuto'):
            logger.info('会议对话框为开启状态')
            return True
        else:
            logger.info('会议对话框为关闭状态')
            return False

    def open_meeting_dialog(self):
        """打开会议对话框"""
        for i in range(3):
            if self.check_meeting_dialog():
                break
            else:
                self.click_meeting_icon()
        else:
            logger.error('打开对话框失败')
            assert 0

    def close_meeting_dialog(self):
        """关闭会议对话框"""
        for i in range(3):
            if self.check_meeting_dialog():
                self.click_meeting_icon()
            else:
                break
        else:
            logger.error('关闭对话框失败')
            assert 0

    def click_meeting_icon(self):
        """点击会议图标--耳机icon"""
        self.click_by_condition('xpath', '//div[@class="audio-meeting-container"]/div/span[1]', '会议区域icon')

    def click_voice_in_meeting_dialog_view(self):
        """会议对话框点击静音"""
        self.click_by_condition('class', 'audio-mute', '对话框-静音', 5)

    def check_if_silent_in_meeting_dialog_view(self):
        """通过会议面板检测是否静音"""
        voice_ele = self.find_by_condition('xpath', '//div[@class="audio-mute"]/span')
        voice_class = voice_ele.get_attribute('class')
        logger.info(voice_class)
        if 'iconmic-off' in voice_class:
            logger.info('检测到当前为静音状态')
            return True
        elif 'iconmic' in voice_class:
            logger.info('检测到当前为非静音状态')
            return False
        else:
            logger.error('检测语音状态异常')
            assert 0

    def check_voice_status_in_meeting_dialog_view(self, silent=False):
        """对比静音点击后的结果(对话框页面)"""
        if (silent and self.check_if_silent_in_meeting_dialog_view()) or (
                not silent and not self.check_if_silent_in_meeting_dialog_view()
        ):
            return True
        else:
            logger.error('实际状态和操作不一致')
            assert 0

    def click_voice_in_meeting_title(self):
        """会议对话框点击静音"""
        if self.check_if_silent_in_meeting_title():
            self.click_by_condition('xpath', '//div[@class="audio-meeting-container"]/div/span[3]', '标题-静音')
        else:
            self.click_by_condition('xpath', '//div[@class="audio-meeting-container"]/div/span[2]', '标题-静音')

    def check_if_silent_in_meeting_title(self):
        """通过会议面板检测是否静音"""
        on_ele = self.find_by_condition('xpath', '//div[@class="audio-meeting-container"]/div/span[2]')
        off_ele = self.find_by_condition('xpath', '//div[@class="audio-meeting-container"]/div/span[3]')
        if off_ele.get_attribute("style"):
            logger.info('检测到当前为非静音状态')
            return False
        elif on_ele.get_attribute("style"):
            logger.info('检测到当前为静音状态')
            return True
        else:
            logger.error('检测语音状态异常')
            assert 0

    def check_voice_status_in_meeting_title(self, silent=False):
        """对比静音点击后的结果"""
        if (silent and self.check_if_silent_in_meeting_title()) or (
                not silent and not self.check_if_silent_in_meeting_title()
        ):
            return True
        else:
            logger.error('实际状态和操作不一致')
            assert 0

    def wait_meeting_loading(self):
        """等待会议加载"""
        time.sleep(10)
        return
        cur_time = time.time()
        while time.time() - cur_time <= 30:
            time.sleep(5)
            if self.find_by_condition('class', 'el-loading-mask').get_attribute('style'):
                logger.info('会议加载中。。。')
            else:
                logger.info('会议加载完成')
                time.sleep(5)
                return True
        else:
            logger.error('会议加载超时')
            assert 0

    def join_meeting_by_link(self, url=''):
        """点击链接加入会议"""
        self.open_page(url)
        self.refresh()
        self.click_by_text('div', '加入会议', timeout=5)
        self.click_by_img('firefox_allow_voice', '允许录音权限')
        self.wait_meeting_loading()

    def join_meeting_by_button(self):
        """点击按钮加入会议"""
        self.refresh()
        self.click_by_condition('class', 'join-wrap', '加入')
        self.wait_meeting_loading()

    def get_meeting_member_list(self):
        """获取会议成员列表"""
        name_ele = self.finds_by_condition('class', 'member-name')
        name_list = [self.get_text(n) for n in name_ele]
        return name_list

    def check_join_meeting(self, user_name=parse.usr_2_name):
        """检测加入会议是否成功"""
        if user_name in self.get_meeting_member_list():
            logger.info('加入会议成功')
        else:
            logger.error('加入会议失败')
            assert 0

    def check_host_translate(self):
        """检测主持人移交状态"""
        for i in range(5):
            time.sleep(5)
            if self.check_condition('class', 'alert'):
                logger.info('检测到主持人自动分配弹窗')
                break
        else:
            logger.error('未检测到主持人自动分配弹窗')
            assert 0
        self.click_by_text('div', '知道了')
        if self.check_condition('xpath', '//span[text()="(我)"]/../../div[text()="主持人"]'):
            logger.info('主持人移交成功')
        else:
            logger.error('主持人移交失败')
            assert 0

    def remove_meeting_member(self, user_name):
        """移除会议成员"""
        remove_xpath = f'//span[text()="{user_name}"]/../../..//div[@class="hostOptWrap"]/div[2]'
        self.click_by_condition('xpath', remove_xpath, f'移除用户--{user_name}')
        self.wait_until_text(text=f'{user_name}已经被移出会议')
        if user_name not in self.get_meeting_member_list():
            logger.info('会议成员移除成功')
            time.sleep(3)
        else:
            logger.error('成员仍在会议成员列表中，移除失败')
            assert 0

    def get_player_count(self):
        """获取播放器数量"""
        player_count = len(self.finds_by_condition('class', 'player-content'))
        logger.info(f'播放器数量为：{player_count}')
        return player_count

    def check_player_count(self, player_count=1):
        """检测播放器数量是否和选项一致"""
        if self.get_player_count() == player_count:
            logger.info('播放器数量检测成功')
        else:
            logger.info('播放器数量检测异常')
            assert 0

    def get_camera_file_list(self):
        """获取机位文件列表"""
        file_name_ele_list = self.finds_by_condition('xpath', '//div[@class="file-list-info"]//p[1]/span')
        file_name_list = [self.get_text(f) for f in file_name_ele_list]
        return file_name_list

    def get_video_player_time(self, player_index=1):
        """获取播放器播放时间"""
        time_ele = self.finds_by_condition('class', 'player-ctrl__curTime')[player_index * 2 - 1]
        play_time = self.get_text(time_ele).split('/')[0].strip()
        logger.info(f'当前播放器时间为：{play_time}')
        return play_time

    def get_video_player_duration(self, player_index=1):
        """获取视频总时长"""
        duration_ele = self.finds_by_condition('class', 'player-ctrl__duration')[player_index * 2 - 1]
        return self.get_text(duration_ele)[3:]

    @staticmethod
    def get_player_seconds(p_time=''):
        """解析播放器时间为秒数"""
        time_list = p_time.split(':')
        sec = 0
        for i, t in enumerate(time_list):
            sec += int(t) * 60 ** (len(time_list) - i - 1)
        return sec

    def select_video_play(self):
        """选择视频文件播放"""
        for index, file_name in enumerate(self.get_camera_file_list()):
            if self.is_video(file_name):  # 检测视频文件
                self.click_by_condition_index('class', 'file-list-info', index + 1)
                break
        else:
            logger.error('未检测到视频文件，终止测试')
            assert 0

    def check_many_player(self, count=1):
        """多屏检测"""
        player_dict = {'双屏': 2,
                       '四屏': 4}
        #  遍历测试单屏、双屏、四屏
        for player_button, player_count in player_dict.items():
            self.click_by_text(text=player_button, timeout=5)
            self.check_player_count(player_count)
            for i in range(player_count):  # 检测多个播放器是否正常播放
                self.click_by_condition_index('class', 'iconalign-right', i, '打开视频列表')
                self.select_video_play()
                self.click_by_condition('class', 'showIcon', '关闭视频列表')
                if self.get_video_player_duration(i + 1) == '':
                    logger.info('获取视频时长异常')
                    assert 0
                self.click_by_condition_index('xpath', '//div[@class="control-item"]/div[1]/div[1]/div[1]', i, '播放', 3)
                cur_player_time = self.get_player_seconds(self.get_video_player_time(i + 1))
                if cur_player_time >= 2:
                    logger.info('播放成功')
                else:
                    logger.error('播放时间异常')
                    assert 0
                self.click_by_condition_index('xpath', '//div[@class="control-item"]/div[1]/div[1]/div[1]', i, '暂停')

    def video_player_start(self):
        """视频播放"""
        if self.check_condition('class', 'iconzanting_zanting'):
            logger.info('当前播放器为播放状态')
        else:
            self.click_by_condition_index('class', 'player-ctrl__item', 0, '播放', 0)

    def video_player_stop(self):
        """点击播放器开关"""
        if self.check_condition('class', 'iconzanting_zanting'):
            logger.info('当前播放器为播放状态')
            self.click_by_condition('class', 'iconzanting_zanting', '暂停', 0)
        else:
            logger.info('当前播放器为暂停状态')

    def check_player_status(self, play=True):
        """
        检测视频播放状态
        :param play:  播放状态 True/False
        """
        compare_result = self.compare_time()
        if play:
            if compare_result > 0:
                logger.info('播放成功')
            else:
                logger.error('播放失败')
                assert 0
        else:
            if compare_result == 0:
                logger.info('暂停播放成功')
            else:
                logger.error('暂停播放失败')
                assert 0

    def compare_time(self, timeout=3):
        cur_play_time = self.get_video_player_time()
        logger.info(f'等待{timeout}秒后再次检测')
        time.sleep(timeout)
        play_time = self.get_video_player_time()
        return self.get_player_seconds(play_time) - self.get_player_seconds(cur_play_time)

    def control_player_forward(self, step=3):
        """控制播放器前进 step--播放器前进秒数"""
        duration_seconds = self.get_player_seconds(self.get_video_player_duration())  # 获取视频总时长
        cur_player_seconds = self.get_player_seconds(self.get_video_player_time())  # 获取点击前播放器时间
        self.click_by_condition('class', 'iconqianjin', '前进')
        player_seconds = self.get_player_seconds(self.get_video_player_time())  # 获取点击后播放器时间
        if duration_seconds - cur_player_seconds <= step:  # 如果前进之前的时间和总时长差值小于前进秒数，则点击后秒数和总时长一致
            if player_seconds == duration_seconds:
                logger.info(f'快进{step}秒成功')
            else:
                logger.error(f'快进{step}秒失败')
                assert 0
        else:  # 如果前进之前的时间和总时长差值大于前进秒数，则点击前后秒数差值为前进秒数
            if player_seconds - cur_player_seconds == step:
                logger.info(f'快进{step}秒成功')
            else:
                logger.error(f'快进{step}秒失败')
                assert 0

    def control_player_back(self, step=3):
        """控制播放器后退  step--播放器前进秒数"""
        cur_player_seconds = self.get_player_seconds(self.get_video_player_time())  # 获取点击前播放器时间
        self.click_by_condition('class', 'iconhoutui', '后退')
        player_seconds = self.get_player_seconds(self.get_video_player_time())  # 获取点击后播放器时间
        if cur_player_seconds <= step:  # 如果当前时间小于后退秒数，则点击后秒数为0
            if player_seconds == 0:
                logger.info(f'快退{step}秒成功')
            else:
                logger.error(f'快退{step}秒失败')
                assert 0
        else:  # 如果后退之前的秒数大于后退秒数，则点击前后秒数差值为后退秒数
            if cur_player_seconds - player_seconds == step:
                logger.info(f'快退{step}秒成功')
            else:
                logger.error(f'快退{step}秒失败')
                assert 0

    def change_video_time_code_to_code(self):
        """时间码格式修改--时间码"""
        self.click_by_condition_index('class', 'player-ctrl__curTime', 0)
        self.click_by_condition_index('xpath', '//div[text()="时间码"]', -1, '时间码')
        player_time = self.get_video_player_time()
        check_list = player_time.split(':')
        if len(check_list) == 4:
            logger.info('时间码格式切换为--时间码 成功')
        else:
            logger.error('时间码格式切换为--时间码 失败')
            assert 0

    def change_video_time_code_to_fps(self):
        """时间码格式修改--帧"""
        self.click_by_condition_index('class', 'player-ctrl__curTime', 0)
        self.click_by_condition_index('xpath', '//div[text()="帧"]', -1, '帧')
        player_time = self.get_video_player_time()
        if ':' in player_time:
            logger.error('时间码格式切换为--帧 失败')
            assert 0
        else:
            logger.info('时间码格式切换为--帧 成功')

    def control_fps_forward(self):
        """视频文件切换下一帧"""
        cur_fps = self.get_video_player_time()
        self.click_by_condition('class', 'iconskip_forward2', '下一帧')
        fps = self.get_video_player_time()
        if int(fps) - int(cur_fps) == 1:
            logger.info('切换下一帧成功')
        else:
            logger.error('切换下一帧失败')
            assert 0

    def control_fps_back(self):
        """视频文件切换上一帧"""
        cur_fps = self.get_video_player_time()
        self.click_by_condition('class', 'iconskip-back2', '上一帧')
        fps = self.get_video_player_time()
        if int(cur_fps) - int(fps) == 1:
            logger.info('切换上一帧成功')
        else:
            logger.error('切换上一帧失败')
            assert 0

    def change_video_time_code_to_normal(self):
        """时间码格式修改--标准"""
        self.click_by_condition_index('class', 'player-ctrl__curTime', 0)
        self.click_by_condition_index('xpath', '//div[text()="标准"]', -1, '标准')
        player_time = self.get_video_player_time()
        check_list = player_time.split(':')
        if len(check_list) == 2:
            logger.info('时间码格式切换为--标准 成功')
        else:
            logger.error('时间码格式切换为--标准 失败')
            assert 0

    def video_sound_control(self):
        """点击音量控制"""
        self.click_by_condition_index('class', 'player-ctrl__item', 5, '音量控制', 3)

    def is_no_sound(self):
        """检测是否静音状态"""
        voice_img = self.find_by_condition('xpath', '//img[@class="icon"]')
        src = voice_img.get_attribute('src').strip()
        if 'AAAJu' in src:  # 非静音图片地址带有aGG字符串
            logger.info('检测到音量图标为非静音图片')
            return False
        else:
            logger.info('检测到音量图标为静音图片')
            return True

    def video_sound_close(self):
        """静音"""
        self.video_sound_control()
        if self.is_no_sound():
            return True
        else:
            assert 0

    def video_sound_open(self):
        """取消静音"""
        self.video_sound_control()
        if self.is_no_sound():
            assert 0
        else:
            return True

    def change_video_views_quality(self):
        """修改视频播放画质"""
        current_quality = self.finds_by_condition('class', 'player-ctrl__item--hover')[-5]
        self.click_by_condition_index('class', 'player-ctrl__item', -5, '画质切换')
        quality_ele_list = self.finds_by_condition('xpath', '//div[@class="definition-list-item"]//span')
        if len(quality_ele_list) == 1:
            logger.info('画质选项为1，无法切换')
            return True
        next_quality = self.get_text(quality_ele_list[1])
        logger.info(f'下一个画质为：{next_quality}')
        self.click_by_condition_index('class', 'definition-list-item', 1, next_quality, 5)
        if self.get_text(current_quality) == next_quality:
            logger.info('画质切换成功')
        else:
            logger.error('画质切换失败')
            assert 0

    def change_video_player_speed(self):
        """修改视频播放速度"""
        current_speed = self.finds_by_condition('class', 'player-ctrl__item--hover')[-4]
        self.click_by_condition_index('class', 'player-ctrl__item', -4, '倍数切换')
        self.click_by_condition('xpath', '//html/body/ul/li//div[contains(text(), "2.0")]', '2.0倍数')
        if '2.0' in self.get_text(current_speed):
            logger.info('当前倍数为2.0')
        else:
            logger.error('倍数不为2.0')
            assert 0
        self.video_player_start()
        logger.info('等待五秒检测播放器时间')
        time.sleep(5)
        player_time = self.get_player_seconds(self.get_video_player_time())
        if player_time >= 8:  # 允许有部分误差
            logger.info('倍数切换成功')
        else:
            logger.error('播放器时间和倍数不一致')
            self.video_player_stop()
            assert 0
        self.video_player_stop()

    def file_max_view(self):
        """文件全屏显示"""
        self.click_by_condition('class', 'iconquanping_quanpin', '全屏')  # 点击全屏
        if self.check_condition('class', 'viewer-container'):  # 图片文件判断全屏
            player = self.find_by_condition('class', 'viewer-container')  # 获取播放器元素
            player_width = self.get_ele_width(player)  # 获取播放器宽度
            if player_width == screeninfo.get_monitors()[0].width:  # 对比播放器宽度和屏幕宽度
                logger.info('全屏成功')
            else:
                logger.error('全屏失败')
                assert 0
        else:  # 视频文件判断全屏
            if self.check_condition('class', 'iconsuoxiao_suoxiao'):
                logger.info('全屏成功')
            else:
                logger.error('全屏失败')
                assert 0

    def file_quit_max_view(self):
        """文件取消全屏显示"""
        self.click_by_condition('class', 'iconsuoxiao_suoxiao', '取消全屏')  # 点击全屏
        if self.check_condition('class', 'viewer-container'):  # 图片文件判断全屏
            player = self.find_by_condition('class', 'viewer-container')  # 获取播放器元素
            player_width = self.get_ele_width(player)  # 获取播放器宽度
            if player_width < screeninfo.get_monitors()[0].width:  # 对比播放器宽度和屏幕宽度
                logger.info('取消全屏成功')
            else:
                logger.error('取消全屏失败')
                assert 0
        else:  # 视频文件判断全屏
            if self.check_condition('class', 'iconquanping_quanpin'):
                logger.info('取消全屏成功')
            else:
                logger.error('取消全屏失败')
                assert 0

    def back_to_shoot_index(self):
        """返回拍摄首页"""
        for i in range(5):
            if self.check_text(text='我的拍摄'):
                logger.info('当前在拍摄首页')
                break
            else:
                if self.check_condition('class', 'iconfanhui_fanhui'):
                    self.click_by_condition('class', 'iconfanhui_fanhui', '返回', 3)
        else:
            logger.error('未返回到拍摄首页')
            assert 0

    def set_read_status(self, status='主推'):
        """设置审阅状态"""
        self.click_by_condition('xpath', f'//div[@class="label-content"]//div[contains(text(), "{status}")]', status)
        time.sleep(5)

    def check_read_status(self, status='主推'):
        """检查审阅状态"""
        if self.check_condition('xpath', f'//div[@class="file-list checkedBack"]//span[text()="{status}"]'):
            logger.info('检测到审阅状态icon')
            return True
        else:
            logger.error('未检测到审阅状态icon')
            assert 0

    def open_left_view(self):
        """打开左侧侧边栏"""
        self.click_by_condition('class', 'iconcebianlanout', '展开左侧侧边栏')
        if self.check_text(text='批量操作'):
            logger.info('检测到「批量操作」，侧边栏展开成功')
            return True
        else:
            logger.error('未检测到「批量操作」，侧边栏展开失败')
            assert 0

    def close_left_view(self):
        """收起左侧侧边栏"""
        self.click_by_condition('class', 'iconcebianlanin', '收起左侧侧边栏')
        if self.check_text(text='批量操作'):
            logger.error('检测到「批量操作」，侧边栏收起失败')
            assert 0
        else:
            logger.info('未检测到「批量操作」，侧边栏收起成功')
            return True

    def get_current_camera_in_detail(self):
        """获取当前选中的机位"""
        select_ele = self.find_by_condition('class', 'is-active')
        select_id = select_ele.get_attribute('id')
        return select_id

    def get_current_camera_file_count(self):
        """获取当前机位文件数"""
        camera_id = self.get_current_camera_in_detail()
        camera_ele = self.find_by_condition('xpath', f'//div[@id="{camera_id}"]/span')
        file_count = int(re.findall(r'\((\d+)\)', self.get_text(camera_ele))[0]) - 1
        logger.info(f'当前机位文件数为：{file_count}')
        return file_count

    def select_all_files(self):
        """全选"""
        self.click_by_text(text='批量操作')
        self.click_by_text(text='全选')

    def download_files(self):
        """下载文件"""
        self.click_by_condition('xpath', '//div[@class="user-opt-wrap"]/div[contains(text(), "下载")]', '下载')
        self.click_by_text(text='确认下载')
        self.click_by_img('allow_download', '允许下载多个文件')  # 浏览器授权允许下载多个文件
        time.sleep(10)
        file_count = self.get_current_camera_file_count()
        self.check_download(file_count)

    def copy_files_to_shoot(self):
        """复制文件"""
        self.click_by_condition('xpath', '//div[@class="user-opt-wrap"]/div[contains(text(), "复制")]', '复制')
        time.sleep(3)
        self.click_by_condition_index('class', 'tab-item', 2, '拍摄')
        self.click_by_condition('xpath',
                                f'//div[@class="dialog-wrapper"]//div[contains(text(), "{parse.project_name}")]')
        self.click_by_condition('xpath',
                                f'//div[@class="dialog-wrapper"]//div[contains(text(), "{parse.copy_camera}")]')
        self.click_by_text(text='确定')
        logger.info('等待10秒钟复制完成')
        time.sleep(10)
        # if self.wait_until_text(text='您复制到拍摄的文件已成功', timeout=30):  # 检测通知
        #     logger.info('检测到复制成功通知')
        # else:
        #     logger.error('未检测到复制成功通知')
        #     assert 0

    def select_camera(self, camera=parse.camera):
        self.click_by_condition('xpath', f'//span[contains(text(), "{camera}")]', camera)

    def check_copy_to_shoot(self):
        """检测复制到拍摄是否成功"""
        self.select_camera(parse.camera)
        file_count = self.get_current_camera_file_count()
        self.select_camera(parse.copy_camera)
        copy_count = self.get_current_camera_file_count()
        if file_count == copy_count:
            logger.info('复制成功')
            return True
        else:
            logger.error('文件数不一致，复制失败')
            assert 0

    def copy_to_media(self):
        """复制到资源"""
        shoot_handle = self.driver.current_window_handle
        self.open_another_page(f'{self.url}media/all')
        media_handle = self.get_another_page()
        self.driver.switch_to.window(media_handle)
        time.sleep(10)
        cur_count = self.get_media_file_count()
        self.driver.switch_to.window(shoot_handle)
        copy_count = self.get_current_camera_file_count()
        self.click_by_condition('xpath', '//div[@class="user-opt-wrap"]/div[contains(text(), "复制")]', '复制')
        time.sleep(3)
        self.click_by_condition_index('class', 'tab-item', 1, '资源')
        self.click_by_text(text='全部资源')
        self.click_by_text(text='确定')
        logger.info('等待10秒钟复制完成')
        time.sleep(10)
        # if self.wait_until_text(text='您复制到资源的文件已成功', timeout=30):  # 检测通知
        #     logger.info('检测到复制成功通知')
        # else:
        #     logger.error('未检测到复制成功通知')
        #     assert 0
        self.driver.switch_to.window(media_handle)
        self.refresh()
        if self.get_media_file_count() == cur_count + copy_count:
            logger.info('文件数检测完成，复制到资源成功')
            self.driver.close()
            self.driver.switch_to.window(shoot_handle)
            return True
        else:
            logger.error('文件数检测完成，复制到资源失败')
            self.driver.close()
            self.driver.switch_to.window(shoot_handle)
            assert 0

    def delete_files(self):
        """删除文件"""
        self.click_by_condition('xpath', '//div[@class="user-opt-wrap"]/div[contains(text(), "删除")]', '删除')
        self.click_by_condition('xpath', '//*[@class="alert"]//div[text()="删除 "]', '删除', 1)
        self.wait_until_xpath('//p[contains(text(), "删除文件成功")]')
        logger.info('删除成功！')

    def check_delete(self, camera=parse.copy_camera):
        """检测删除文件是否成功"""
        self.select_camera(camera)
        if self.get_current_camera_file_count() == 0:
            logger.info('文件删除成功')
            return True
        else:
            logger.error('文件删除失败')
            assert 0

    def hide_left_view(self):
        """隐藏左边侧边栏"""
        self.click_by_condition('class', 'showIcon', '隐藏左边侧边栏')
        left_ele = self.find_by_condition('class', 'shoot-content-left')
        left_class = left_ele.get_attribute('class')
        if 'width0' in left_class:
            logger.info('检测到左边侧边栏宽度为0，隐藏成功')
            return True
        else:
            logger.error('检测到左边侧边栏宽度不为0，隐藏失败')
            assert 0

    def show_left_view(self):
        """显示左边侧边栏"""
        self.click_by_condition('class', 'showIcon', '显示左边侧边栏')
        left_ele = self.find_by_condition('class', 'shoot-content-left')
        left_class = left_ele.get_attribute('class')
        if 'width0' in left_class:
            logger.error('检测到左边侧边栏宽度为0，显示失败')
            assert 0
        else:
            logger.info('检测到左边侧边栏宽度不为0，显示成功')
            return True

    def get_current_file_name(self):
        """获取当前文件名"""
        file_name_ele = self.find_by_condition('xpath',
                                               '//div[@class="file-list checkedBack"]//div[@class="file-list-info"]/p[1]/span')
        file_name = self.get_text(file_name_ele)
        logger.info(f'当前文件名为：{file_name}')
        return file_name

    def file_rename(self, new_name='rename'):
        """文件重命名"""
        rename_ele = self.find_by_condition('class', 'link-input')
        rename_ele.clear()
        rename_ele.send_keys(new_name)
        time.sleep(1)
        pyautogui.press('Return')  # 回车确定
        time.sleep(3)
        # self.wait_until_text(text='编辑文件名成功')

    def check_rename(self, new_name='rename'):
        """检测重命名是否成功"""
        file_name = self.get_current_file_name().split('.')[0]
        if file_name == new_name:
            logger.info('文件名修改成功')
            return True
        else:
            logger.error('文件名修改失败')
            assert 0

    def get_file_grade(self):
        # 通过获取星星元素数量判断当前评分
        grade_num = len(self.finds_by_condition('class', 'starFill'))
        logger.info(f'当前评分为--{grade_num}')
        return grade_num

    def change_file_grade_by_info(self):
        """修改文件评分"""
        cur_grade = self.get_file_grade()  # 获取当前评分
        if cur_grade == 5:  # 5星则评分降低，否则默认加1星测试
            change_grade = 4
        else:
            change_grade = cur_grade + 1
        logger.info(f'设置评分为：{change_grade}颗🌟')
        # python索引比实际序列小1位
        self.click_by_condition_index('xpath', '//div[@class="rateIconWrap"]/span', change_grade - 1)
        if self.get_file_grade() == change_grade:  # 判断打分后结果和打分是否一致
            logger.info('评分设置成功')
        else:
            logger.error('评分设置失败')
            assert 0

    def add_discussion(self, info='这是一条评论'):
        """添加审批意见"""
        self.click_by_text(text='审评意见')
        input_ele = self.find_by_condition('id', 'input-area')
        input_ele.clear()
        input_ele.send_keys(info)
        self.click_by_text(text='发送', timeout=5)

    def check_discussion(self, info='这是一条评论'):
        first_dis_ele = self.finds_by_condition('xpath', '//span[@class="comment-item-content-text"]/span')[0]
        first_dis = self.get_text(first_dis_ele)
        if first_dis == info:
            logger.info('添加意见成功')
            return True
        else:
            logger.error('添加意见失败')
            assert 0

    def check_role_read_permission(self, role='审阅者'):
        """检测角色查看文件权限"""
        select_ele = self.find_by_condition('xpath', f'//li[contains(text(), "{role}")]/span')
        if select_ele.get_attribute('class') == 'notChecked':
            logger.info(f'当前角色：{role} 无查看文件权限')
            return False
        else:
            logger.info(f'当前角色：{role} 拥有查看文件权限')
            return True

    def set_role_read_permission(self, role='审阅者', read=True):
        select_ele = self.find_by_condition('xpath', f'//li[contains(text(), "{role}")]/span')
        if self.check_role_read_permission(role):
            if read:
                pass
            else:
                logger.info('关闭查看文件权限')
                select_ele.click()
                time.sleep(1)
        else:
            if read:
                logger.info('打开查看文件权限')
                select_ele.click()
                time.sleep(1)
            else:
                pass
        self.click_by_text(text='保存设置', timeout=0)
        self.wait_until_text(text='保存成功')

    def get_project_room(self):
        """获取拍摄项目存储空间"""
        room = self.get_text(self.find_by_condition('xpath', '//span[contains(text(), "存储空间：")]/..'))
        logger.info(f'当前项目存储空间为：{room}')
        return room

    def check_close_read_permission_by_room(self):
        """检测关闭查看文件权限是否设置成功"""
        if '*' in self.get_project_room():
            logger.info('检测到无法查看项目存储空间')
        else:
            logger.error('能查看项目空间，关闭权限失败')
            assert 0

    def check_close_read_permission_by_file(self):
        """检测关闭查看文件权限是否设置成功"""
        if self.get_camera_file_list():
            logger.error('能看到机位文件，关闭权限失败')
            assert 0
        else:
            logger.info('检测到无法查看机位文件')
            return True

    def select_camera_to_share(self, camera=parse.camera):
        """选中机位分享"""
        logger.info(f'选择机位-{camera}')
        self.click_by_condition('xpath',
                                f'//span[contains(text(), "{camera}")]/../../..//div[@class="select-icon flex-row flex-all-center"]')

    def create_share_link(self):
        """创建分享"""
        self.click_by_condition('class', 'iconfenxiang_fenxiang', '创建分享')
        self.select_camera_to_share()
        self.click_by_condition('class', 'share-btn', '分享', 3)
        if self.check_text(text='创建拍摄分享'):
            logger.info('检测到分享弹窗')
        else:
            logger.error('未检测到分享弹窗')
            assert 0
        self.click_by_condition('class', 'confirm', '创建', 5)
        share_url = self.get_text(self.find_by_condition('xpath', '//span[contains(text(), "链接：")]/../span[2]'))
        self.click_by_text(text='复制链接')
        if share_url in self.get_copy_text():
            logger.info('复制链接成功')
        else:
            logger.error('复制链接失败')
            self.close_share_view()
            assert 0
        self.close_share_view()
        return share_url

    def check_open_share_link(self, read=True):
        """
        检测分享落地页
        :param read: 是否支持文件查看
        """
        if self.get_camera_file_list():
            logger.info('检测到文件列表')
            if read:
                logger.info('分享功能正常')
                return True
            else:
                logger.error('分享功能异常')
                assert 0
        else:
            logger.info('未检测到文件列表')
            if read:
                logger.error('分享功能异常')
                assert 0
            else:
                logger.info('分享功能正常')
                return True

    def close_share_view(self):
        """关闭分享弹窗"""
        self.click_by_condition('class', 'iconquxiao_quxiao', '关闭分享弹窗')

