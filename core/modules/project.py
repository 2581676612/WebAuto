import os
import random
import re

import pytest
import screeninfo
import shutil
import time
import pyautogui
import core.base.parse as parse

from core.base.logger import logger
from core.modules.control import Control
import selenium.common.exceptions as ex


class Project(Control):
    def enter_project_view(self):
        """进入项目首页"""
        url = self.url + 'project'
        self.open_page(url)

    def back_to_project_index(self):
        """返回项目首页"""
        self.enter_project_view()
        time.sleep(3)

    def open_project_menu(self, p_name=parse.project_name):
        """打开项目菜单栏"""
        try:
            setting_ele = self.finds_by_condition('xpath', f'//span[contains(text(), "{p_name}")]/../div[2]')
            if len(setting_ele) > 1:
                logger.info('检测到相关项目不止一个，默认使用第一个测试')
            setting_ele[0].click()
            time.sleep(1)
        except:
            logger.error('未找到测试项目，请检查项目是否存在！')
            assert 0

    def open_project_settings(self, setting='项目设置', timeout=2):
        """打开项目设置"""
        self.click_by_condition_index('xpath', f'//div[contains(text(), "{setting}")]', -1, f'{setting}', timeout)

    def close_project_setting(self):
        """关闭项目设置"""
        self.click_by_condition_index('xpath', '//div[@class="dialog-header"]//i', -1, '关闭项目设置')

    def touch_to_project(self):
        """选择、打开项目"""
        project_ele_list = self.finds_by_condition('xpath',
                                                   '//span[contains(text(), "我的项目")]/../..//ul[@class="cardList"]/div[1]/div[@class="cardList-clone-wrapper"]')
        for project_ele in project_ele_list:
            if project_ele.get_attribute('innerText') == parse.project_name:
                logger.info('检测到测试项目，点击打开')
            project_ele.click()
            time.sleep(1)
            break
        else:
            logger.error('未找到测试项目，请检查项目是否存在！')
            assert 0

    def set_permission(self):
        """权限设置"""
        self.click_by_condition('xpath', '//p[contains(text(), "身份权限设置")]/../../div[2]/div', '打开权限设置')

    def set_fangluping(self, open=True):
        """设置防录屏"""
        fangluping_ele = self.find_by_condition('xpath', '//p[contains(text(), "防录屏")]/../../div[2]/div')
        if open:
            if fangluping_ele.get_attribute('aria-checked'):
                logger.info('防录屏开关为打开状态')
            else:
                logger.info('防录屏开关未打开，点击打开')
                fangluping_ele.click()
                self.wait_until_text(text='操作成功')
        else:
            if fangluping_ele.get_attribute('aria-checked'):
                logger.info('防录屏开关为打开状态，点击关闭')
                fangluping_ele.click()
                self.wait_until_text(text='操作成功')
            else:
                logger.info('防录屏开关为未打开状态')
        time.sleep(2)
        self.close_project_setting()

    def check_project_has_file(self):
        """检测项目内是否存在文件"""
        if self.driver.find_element('class', 'file-list'):
            logger.info('检测到项目内存在文件')
        else:
            logger.info('检测到项目内不存在文件')

    def upload_file(self, file='', select_all=False):
        """上传文件"""
        for i in range(5):
            self.click_by_condition('xpath', '//button[contains(text(), "上传/新建")]', '上传/新建')
            self.click_by_condition('class', 'el-upload-dragger', '上传文件', 3)
            if not self.choose_file_to_upload(file, select_all):
                continue
            self.open_upload_page()
            if self.is_file_upload():
                break
            logger.info('文件未正确选取，重试！')
        else:
            pytest.exit('上传失败')

    def upload_dir(self):
        """上传文件夹"""
        for i in range(5):
            self.touch_to_project()
            self.click_by_condition('xpath', '//button[contains(text(), "上传/新建")]', '上传/新建')
            self.click_by_condition('xpath', '//div[contains(text(), "上传")]/../div[2]//div[contains(text(), "文件夹")]',
                                    '上传文件夹', 3)
            if not self.choose_file_to_upload():
                continue
            time.sleep(3)
            self.click_upload_img()
            self.open_upload_page()
            if self.is_file_upload():
                break
            logger.info('文件未正确选取，重试！')
        else:
            pytest.exit('上传失败')

    def delete_all_files(self):
        """删除所有文件"""
        self.open_project()
        while self.check_condition('xpath', '//div[@class="project-title"]/span[contains(text(), "文件")]'):
            logger.info('检测到项目内存在文件/文件夹')
            self.get_project_file_list()[0].click()
            self.click_by_condition('xpath', '//div[contains(text(), "全选")]', '全选')  # 点击全选
            try:
                self.click_by_condition('class', 'moreOpt')
                self.click_by_condition_index('class', 'iconshanchu', -1, '删除')
            except:
                self.click_by_condition('class', 'iconshanchu', '删除')
            time.sleep(3)
            self.click_by_condition('xpath', '//*[@class="alert"]//div[text()="删除 "]', '删除', 1)
            self.wait_until_xpath('//p[contains(text(), "删除成功")]')
            logger.info('删除成功！')
            self.refresh()

    def delete_all_dirs(self):
        """删除所有文件夹"""
        self.touch_to_project()
        while self.check_condition('xpath', '//div[@class="project-title"]/span[contains(text(), "文件夹")]'):
            logger.info('检测到项目内存在文件夹')
            self.click_by_condition('xpath', '//*[@class="directory-info"]//div[@class="el-tooltip more-icon item"]',
                                    '文件夹设置')
            logger.info('点击--删除')
            self.finds_by_condition('xpath', '//div[contains(text(), "删除")]')[-1].click()
            time.sleep(3)
            self.click_by_condition('xpath', '//*[@class="alert"]//div[text()="删除 "]', '删除', 1)
            self.wait_until_xpath('//p[contains(text(), "删除成功")]')
            logger.info('删除成功！')
            self.refresh()

    def delete_file(self, file_name=""):
        """删除项目内文件"""
        if not file_name:
            logger.info('未传入文件，默认删除项目内所有文件')
            self.delete_all_files()
            return True
        self.touch_to_project()
        while self.check_condition('xpath', f'//div[@class="file-subInfo"]//span[contains(text(), "{file_name}")]'):
            self.click_by_condition('xpath',
                                    f'//div[@class="file-subInfo"]//span[contains(text(), "{file_name}")]/../../../../div[@class="el-tooltip more-icon item"]',
                                    '更多设置')
            logger.info('点击--删除')
            self.finds_by_condition('xpath', '//div[contains(text(), "删除")]')[-1].click()
            time.sleep(3)
            self.click_by_condition('xpath', '//*[@class="alert"]//div[text()="删除 "]', '删除', 1)
            self.wait_until_xpath('//p[contains(text(), "删除成功")]')
            logger.info('删除成功！')
            self.refresh()
        else:
            logger.info('未检测到该文件！')

    def delete_dir(self, dir_name=""):
        """删除项目内文件夹"""
        if not dir_name:
            logger.info('未传入文件夹名，默认删除项目内所有文件夹')
            self.delete_all_dirs()
            return True
        self.touch_to_project()
        while self.check_condition('xpath', f'//div[@class="directory-info"]//span[contains(text(), "{dir_name}")]'):
            self.click_by_condition('xpath', f'//div[@class="directory-info"]//span[contains(text(), "{dir_name}")]\
                                                /../../../../div[@class="el-tooltip more-icon item"]', '更多设置')
            logger.info('点击--删除')
            self.finds_by_condition('xpath', '//div[contains(text(), "删除")]')[-1].click()
            time.sleep(3)
            self.click_by_condition('xpath', '//*[@class="alert"]//div[text()="删除 "]', '删除', 1)
            self.wait_until_xpath('//p[contains(text(), "删除成功")]')
            logger.info('删除成功！')
            self.refresh()
        else:
            logger.info('未检测到该文件！')

    def check_video_in_project(self):
        """检测项目内是否存在视频文件"""
        project_file_list = self.finds_by_condition('xpath', '//div[@class="subInfo-title"]/span')  # 获取项目内文件名
        for project_file in project_file_list:
            file_name = project_file.get_attribute('innerText')
            if '.' in file_name:
                file_type = file_name.split('.')[-1]
                if file_type in parse.file_type_dict['video']:
                    logger.info(f'检测到存在视频类文件--{file_name}')
                    break
        else:
            logger.info('未检测到视频文件，自动上传')
            self.upload_file('video.mp4')
            self.wait_upload()

    def check_fangluping(self, open=True):
        """检测防录屏
            open--防录屏状态True/False
        """
        if open:
            if self.check_condition('class', 'mark-bg'):
                logger.info('检测到防录屏标志')
                return True
            else:
                logger.error('未检测到防录屏标志')
                assert 0
        else:
            if self.check_condition('class', 'mark-bg'):
                logger.error('检测到防录屏标志')
                assert 0
            else:
                logger.info('未检测到防录屏标志')
                return True

    def create_project_quickly(self, p_name=parse.project_name):
        """快速创建项目（只填写文件名）"""
        self.click_by_condition('class', 'iconjiahao_jiahao', '左上角加号图标', 3)
        logger.info('输入项目名称')
        self.find_by_condition('class', 'el-input__inner').send_keys(p_name)
        # 点击完成创建
        self.click_by_condition('xpath', '//span[contains(text(), "完成创建")]', '完成创建', 1)
        # 等待检测到创建项目成功提示
        if self.wait_until_xpath('//p[contains(text(), "创建项目成功")]'):
            logger.info('检测到提示--创建项目成功')
            time.sleep(3)
        else:
            logger.error('未检测到项目创建成功提示！')
            assert 0

    def create_project(self):
        """创建项目"""
        flag_color_dict = {1: ['无色', 'None'],
                           2: ['蓝色', 'rgb(52, 109, 254)'],
                           3: ['粉色', 'rgb(255, 114, 116)'],
                           4: ['黄色', 'rgb(252, 197, 16)'],
                           5: ['紫色', 'rgb(104, 87, 255)'],
                           6: ['绿色', 'rgb(2, 196, 169)'],
                           7: ['橙色', 'rgb(241, 143, 96)']
                           }
        # 随机选择标记颜色
        choose_color_num = random.randint(1, 7)
        color = flag_color_dict.get(choose_color_num)[0]
        self.click_by_condition('class', 'iconjiahao_jiahao', '左上角加号图标')
        logger.info('输入项目名称')
        self.find_by_condition('class', 'el-input__inner').send_keys(parse.project_name)
        logger.info(f'选择标记颜色--{color}')
        if choose_color_num == 1:
            self.find_by_condition('xpath', '//*[@class="color-marker"]/div[@class="clear-icon-box"]').click()
        else:
            self.find_by_condition('xpath',
                                   f'//*[@class="color-marker-wrapper"]/div[@class="color-marker"]/div[{choose_color_num}]/i').click()
        # 点击完成创建
        self.click_by_condition('xpath', '//span[contains(text(), "完成创建")]', '完成创建', 1)
        # 等待检测到创建项目成功提示
        if self.wait_until_xpath('//p[contains(text(), "创建项目成功")]'):
            logger.info('检测到提示--创建项目成功')
            time.sleep(3)
        else:
            logger.error('未检测到项目创建成功提示！')
            assert 0
        # 创建成功后检测标记颜色是否正确
        color_ele = self.find_by_condition('xpath', '//*[@class="cardList"]/div[1]/div[1]/div[1]/i')
        color_style = color_ele.get_attribute('style')
        real_color = ''
        if color_style:
            for key, val in flag_color_dict.items():
                if val[1] in color_style:
                    real_color = val[0]
                    break
        else:
            if choose_color_num == 1:
                real_color = '无色'
        logger.info(f'实际显示颜色为--{real_color}')
        if real_color == color:
            logger.info('标记颜色验证通过！')
        else:
            logger.error('标记颜色验证不通过！')

    def get_my_project_list(self):
        # 获取我的项目列表
        project_ele_list = self.finds_by_condition('xpath',
                                                   '//span[contains(text(), "我的项目")]/../..//ul[@class="cardList"]/div[1]/div[@class="cardList-clone-wrapper"]')
        project_list = [e.get_attribute('innerText') for e in project_ele_list]
        logger.info(f'项目列表为：{project_list}')
        return project_list

    def delete_project(self, project=parse.project_name):
        """删除项目"""
        logger.info('检测是否存在创建的测试项目')
        project_list = self.get_my_project_list()  # 获取项目列表
        while project in project_list:  # 列表内存在测试项目，则删除
            project_ele_list = self.finds_by_condition('xpath',
                                                       '//span[contains(text(), "我的项目")]/../..//ul[@class="cardList"]/div[1]/div[@class="cardList-clone-wrapper"]')
            project_count = len(project_ele_list)
            logger.info(f'项目总数为：{project_count}')
            index = 1
            for ele in project_ele_list:
                p_name = ele.get_attribute('innerText')
                if p_name == project:
                    logger.info('检测到创建测试项目')
                    self.click_by_condition('xpath',
                                            f'//span[contains(text(), "我的项目")]/../..//ul[@class="cardList"]/div[1]/div[{index}]/div[1]/div[2]',
                                            '更多设置')
                    logger.info('点击--删除项目')
                    self.finds_by_condition('xpath', '//div[contains(text(), "删除项目")]')[-1].click()
                    self.click_by_condition('xpath', '//*[@class="space-round"]/div[2]/div[contains(text(), "删除")]',
                                            '删除', 1)
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

    def close_invite_view(self):
        """关闭邀请对话框"""
        self.click_by_condition_index('xpath', '//div[@class="dialog-header-content"]/i', -1, '关闭邀请界面')

    def invite_member(self, usr_name=None, super=True, company=True):
        """邀请成员
        usr_name--企业邀请，根据用户名点击邀请
        super --True 管理员 False 成员
        company --True 企业内邀请 False 链接邀请
        """
        # 选择邀请身份
        self.click_by_condition_index('xpath', '//div[@class="identity-content-select"]', -1, '选择身份')
        if self.is_company():
            identity = '管理者' if super else '查看者'
        else:
            identity = '管理员' if super else '成员'
        self.click_by_condition_index('xpath', f'//div[@class="select-item"]/p[contains(text(), "{identity}")]', -1,
                                      f'{identity}')
        time.sleep(5)
        # 选择邀请方式
        invite_type = "从企业内" if company else "链接扫码"
        self.click_by_condition_index('xpath', f'//p[contains(text(), "{invite_type}")]', -1, invite_type)
        if company:  # 企业内邀请，搜索用户，点击邀请
            self.click_by_condition_index('class', 'search-header-box', -1, '搜索')
            self.finds_by_condition('class', 'search-input')[-1].send_keys(usr_name)
            time.sleep(2)
            result_ele = self.check_condition('xpath', '//div[@class="content-item user-item-box"]')
            if result_ele:
                status = self.finds_by_condition('xpath', '//div[@class="content-item user-item-box"]/span[2]')[
                    0].get_attribute('innerText')
                if '已邀请' in status:
                    logger.info('该用户已被邀请')
                    self.close_invite_view()
                    return True
                self.click_by_condition_index('xpath',
                                              '//div[@class="content-item user-item-box"]/span[contains(text(), "邀请")]',
                                              -1, '邀请')
            if self.wait_until_xpath('//p[contains(text(), "邀请加入成功")]'):
                logger.info('邀请成功')
                self.close_invite_view()
                return True
        else:  # 生成链接邀请
            self.click_by_condition_index('class', 'copy-url-btn', -1, '复制链接')
            if self.wait_until_xpath('//p[contains(text(), "复制链接成功")]'):
                logger.info('复制链接成功')
                url = self.finds_by_condition('class', 'url')[-1].get_attribute('innerText').strip()
                logger.info(url)
                self.close_invite_view()
                return url

    def accept_invite(self, url):
        """点击链接，加入项目"""
        self.open_page(url)  # 打开邀请链接
        if self.check_condition('xpath', '//p[contains(text(), "你已在项目内")]'):  # 已加入
            logger.info('你已在项目内')
            self.click_by_condition('class', 'join-btn')
        elif self.check_condition('class', 'join-btn'):  # 未加入，点击加入
            self.click_by_condition('class', 'join-btn', '加入项目')
            time.sleep(3)
        else:
            logger.error('界面异常')
            assert 0

    def check_join(self):
        """检测加入是否成功"""
        join_pro_list = self.finds_by_condition('xpath', '//div[@class="cardList-clone-wrapper"]')  # 获取加入项目列表
        for join_pro in join_pro_list:  # 判断测试项目是否在加入项目中
            if parse.project_name in join_pro.get_attribute('innerText'):
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

    def close_member_setting_view(self):
        """关闭成员管理界面"""
        self.click_by_condition_index('xpath', '//div[@class="header-content-box"]/i', -1, '关闭成员管理界面')

    def close_share_dialog(self):
        """关闭分享界面"""
        self.click_by_condition('xpath', '//div[@class="dialog-header-content"]/i[2]')

    def close_receive_dialog(self):
        """关闭收集界面"""
        self.click_by_condition('xpath', '//span[contains(text(), "分享到微信")]/../../i')

    def remove_member(self, member=''):
        """删除用户"""
        if not member:  # 未传参，删除所有用户
            logger.info('未检测到用户参数，默认删除所有用户')
        member_ele_list = self.finds_by_condition('class', 'infinite-list-item')  # 获取成员元素列表
        while len(member_ele_list) > 1:  # 成员数大于1，就一直检测
            for i in range(1, len(member_ele_list)):  # 遍历成员列表（删除成员后，列表会变动，需删除后重新获取）
                cur_member = self.find_by_condition('xpath',
                                                    f'//li[@class="infinite-list-item"][{i + 1}]/div[1]/span[1]').get_attribute(
                    'innerText').strip()
                # 未传入用户名，每个用户都删除；传入用户名，删除指定用户
                if (not member) or (member and cur_member == member):
                    self.click_by_condition('xpath',
                                            f'//li[@class="infinite-list-item"][{i + 1}]/div[@class="ops-wrapper"]',
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

    def change_role(self, member='', change_role=''):
        """修改成员角色身份"""
        if not member:  # 检测是否传参
            logger.error('未检测到用户参数!')
            assert 0
        member_ele_list = self.finds_by_condition('class', 'infinite-list-item')  # 获取成员元素列表
        for i in range(1, len(member_ele_list)):
            # 遍历检测成员
            cur_member = self.find_by_condition('xpath',
                                                f'//li[@class="infinite-list-item"][{i + 1}]/div[1]/span[1]'). \
                get_attribute('innerText').strip()
            if cur_member == member:  # 当前成员是要修改的成员
                # 判断当前角色，是管理员就修改为成员，成员修改为管理员
                cur_role = self.find_by_condition('xpath',
                                                  f'//li[@class="infinite-list-item"][{i + 1}]/div[@class="role"]'). \
                    get_attribute('innerText').strip()
                if self.is_company():
                    if change_role == '管理员':
                        change_role = '管理者'
                    elif change_role == '成员':
                        change_role = '查看者'
                    else:
                        change_role = '管理者' if cur_role == '查看者' else '查看者'
                else:
                    change_role = '成员' if cur_role == '管理员' else '管理员'
                # 点击成员设置
                self.click_by_condition('xpath',
                                        f'//li[@class="infinite-list-item"][{i + 1}]/div[@class="ops-wrapper"]',
                                        '设置')
                # 点击要修改的身份
                self.click_by_condition_index('xpath', f'//span[contains(text(), "{change_role}")]', -1,
                                              f'{change_role}')
                # 等待操作成功toast提示
                if self.wait_until_text(text='操作成功') and self.find_by_condition('xpath',
                                                                                f'//li[@class="infinite-list-item"][{i + 1}]/div[@class="role"]'). \
                        get_attribute('innerText').strip() == change_role:
                    logger.info(f'修改成员-{member} 角色成功：{cur_role}->{change_role}')
                    time.sleep(3)
                    break
        else:
            logger.info('未检测到该成员！')
            self.close_member_setting_view()  # 关闭成员管理面板
            assert 0
        self.close_member_setting_view()  # 关闭成员管理面板

    def open_project(self, p_name=parse.project_name):
        """点击项目名，打开项目"""
        try:
            setting_ele = self.finds_by_condition('xpath',
                                                  f'//div[@class="cardList-clone-wrapper"]//span[contains(text(), "{p_name}")]')
            if len(setting_ele) > 1:
                logger.info('检测到相关项目不止一个，默认使用第一个测试')
            setting_ele[0].click()
            time.sleep(1)
        except:
            logger.error('未找到测试项目，请检查项目是否存在！')
            assert 0

    def get_project_file_list(self):
        """获取项目文件列表"""
        return self.finds_by_condition('class', 'card-wrapper')

    def get_project_file_name_list(self):
        """获取项目文件名列表"""
        if self.check_condition('xpath', '//div[@class="project-title"]/span[text()="文件夹"]'):
            name_ele_list = self.finds_by_condition('xpath',
                                                    '//div[@class="file-list"]/div[4]//div[@class="subInfo-title"]')
        else:
            name_ele_list = self.finds_by_condition('xpath',
                                                    '//div[@class="file-list"]/div//div[@class="subInfo-title"]')
        name_list = [self.get_text(e) for e in name_ele_list]
        return name_list

    def select_all_file(self):
        """全选"""
        file_list = self.get_project_file_list()  # 获取所有文件
        file_count = len(file_list)  # 获取文件数
        if file_count == 0:
            logger.error('该项目无文件')
            assert 0
        logger.info('选中文件')
        file_list[0].click()  # 选中第一个文件
        time.sleep(1)
        self.click_by_condition('xpath', '//div[contains(text(), "全选")]')  # 点击全选
        if self.check_condition('xpath', '//div[contains(text(), "取消全选")]'):
            logger.info('检测到「取消全选」，点击全选成功')
        select_count_ele = self.find_by_condition('xpath', '//div[contains(text(), "已选中")]')  # 获取已选中文件文案
        select_count = re.findall(r'(\d+)', self.get_text(select_count_ele))[0]  # 正则获取选中文件数
        if eval(select_count) == file_count:  # 通过文件数判断全选是否成功
            logger.info(f'选中数量「{select_count}」和文件数量「{file_count}」一致，全选成功')
            return True
        else:
            logger.info(f'选中数量「{select_count}」和文件数量「{file_count}」不一致，全选失败')
            self.click_by_text('button', '取消', False)
            assert 0

    def unselect_file(self):
        """取消全选"""
        file_list = self.get_project_file_list()  # 获取项目文件列表
        file_count = len(file_list)  # 获取文件总数
        if file_count == 0:
            logger.error('该项目无文件')
            assert 0
        logger.info('选中文件')
        file_list[0].click()  # 选择第一个文件
        time.sleep(1)
        self.click_by_condition('xpath', '//div[contains(text(), "全选")]')  # 点击全选
        if self.check_condition('xpath', '//div[contains(text(), "取消全选")]'):  # 点击全选后，会出现取消全选文本
            logger.info('检测到「取消全选」，点击全选成功')
        self.click_by_condition('xpath', '//div[contains(text(), "取消全选")]')  # 点击取消全选
        select_count_ele = self.find_by_condition('xpath', '//div[contains(text(), "已选中")]')  # 获取已选中文案
        select_count = re.findall(r'(\d+)', self.get_text(select_count_ele))[0]  # 正则获取选中数量
        if eval(select_count) == 0:  # 通过数量判断是否取消成功
            logger.info('选中数量为0，取消选中成功')
            return True
        else:
            logger.info('选中数量不为0，取消选中失败')
            self.click_by_text('button', '取消', False)
            assert 0

    def cancel_choose_file(self):
        """取消选择文件"""
        self.click_by_text(ele_type='button', text='取消', fuzzy=False)

    def close_choose_file(self):
        """取消选择文件"""
        self.click_by_text('button', '取消', False)

    def get_match_file_index(self, file_type='img'):
        """获取匹配的测试文件索引
            file_type--选择文件类型 img/video/dir
        """
        file_type_list = parse.file_type_dict[file_type]  # 获取该类型文件所有后缀名
        file_ele_list = self.finds_by_condition('xpath', '//div[@class="subInfo-title"]//span')  # 获取所有文件名元素
        content_ele_list = self.finds_by_condition('xpath', '//div[@class="subInfo-content"]//span')
        file_name_list = [self.get_text(f) for f in file_ele_list]  # 提取文件名文本
        file_content_list = [self.get_text(c) for c in content_ele_list]
        for index, name in enumerate(file_name_list):  # 遍历检测是否存在匹配的文件
            if '.' in name:  # 检测文件
                file_behind = name.split('.')[-1]
                if file_behind in file_type_list:
                    logger.info(f'检测到 {file_type} 类型文件--{name}')
                    return index  # 提取文件索引
            else:  # 检测无后缀文件
                if file_type == 'web' and file_content_list[index] == '链接':
                    logger.info(f'检测到链接文件：{name}')
                    return index  # 提取文件索引
                elif file_type == 'dir':
                    logger.info(f'检测到文件夹：{name}')
                    return index  # 提取文件索引
        else:
            logger.error('未找到相匹配测试文件')
            assert 0

    def choose_test_file(self, file_type='', file_name=''):
        """点击选择测试文件
        file_type--选择文件类型 img/video/dir/web
        """
        if file_name:
            self.click_by_condition('xpath', f'//span[text()="{file_name}"]/../../../../../..')
        elif file_type:
            self.get_project_file_list()[self.get_match_file_index(file_type)].click()
        else:
            self.get_project_file_list()[0].click()
        time.sleep(3)

    def choose_other_file(self, file_type='', file_name=''):
        """已选择文件，选择其他文件"""
        if file_name:
            self.click_by_condition('xpath',
                                    f'//span[text()="{file_name}"]/../../../../../..//div[@class="select-circle"]')
        elif file_type:
            self.click_by_condition_index('class', 'select-circle', self.get_match_file_index(file_type))
        else:
            self.get_project_file_list()[0].click()
        time.sleep(3)

    def pre_view(self):
        """点击空格预览"""
        self.click_space()

    def check_pre_view(self):
        """通过检测对话框是否存在，检测预览是否成功"""
        if self.check_condition('class', 'dialog-content'):
            logger.info('检测预览状态成功')
        else:
            logger.error('预览失败')
            assert 0

    def change_file_name_by_info(self, file_type='img'):
        """修改文件名"""
        # 获取文件名元素
        file_index = self.get_match_file_index(file_type)
        file_name_ele = self.finds_by_condition('xpath', '//div[@class="header-folder-box"]//input')[0]
        file_name = file_name_ele.get_attribute('value').strip()  # 获取文件名，首尾去空格
        logger.info(f'当前文件名为：{file_name}')
        file_type = file_name.split('.')[-1]  # 获取文件后缀
        change_name = f'change_name.{file_type}'  # 组合新文件名
        file_name_ele.clear()  # 输入框清空
        file_name_ele.send_keys(change_name)  # 输入新文件名
        time.sleep(1)
        pyautogui.press('Return')  # 回车确定
        time.sleep(5)
        project_file = self.finds_by_condition('xpath', '//div[@class="subInfo-title"]/span')[file_index]  # 获取修改后文件名
        if project_file.get_attribute('innerText').strip() == change_name:  # 对比判断
            logger.info(f'修改文件名--{change_name} 成功')
        else:
            logger.error('修改文件名失败')
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
        self.click_by_condition_index('xpath', '//div[@class="rate-icon-wrap"]/span', change_grade - 1)
        if self.get_file_grade() == change_grade:  # 判断打分后结果和打分是否一致
            logger.info('评分设置成功')
        else:
            logger.error('评分设置失败')
            assert 0

    def change_file_description_by_info(self):
        """修改文件描述"""
        dis_info = '这是一条描述'
        # 获取描述输入框
        description_ele = self.finds_by_condition('xpath', '//div[@class="el-collapse-item__content"]//input')[0]
        description_ele.clear()  # 清空输入框文本
        logger.info('输入描述')
        description_ele.send_keys(dis_info)  # 输入描述
        time.sleep(1)
        pyautogui.press('Return')  # 回车确定
        time.sleep(3)
        cur_description = description_ele.get_attribute('value').strip()  # 获取输入框文本
        logger.info(f'当前描述为：{cur_description}')
        if cur_description == dis_info:  # 判断是否和输入内容一致
            logger.info('描述修改成功')
        else:
            logger.error('描述修改失败')
            assert 0

    def add_file_tag(self, index=0):
        """添加标签"""
        tag_list = self.finds_by_condition('xpath', '//p[contains(text(), "全部标签")]/../ul/li')  # 获取标签列表
        choose_tag = tag_list[index].get_attribute('innerText').strip()  # 获取标签文本
        tag_list[index].click()  # 点击选中标签
        time.sleep(3)
        # self.click_by_text('span', '添加', False)  # 点击添加
        return choose_tag  # 返回选中的标签，后续判断使用

    def change_file_tag_by_info(self):
        """修改文件标签"""
        self.click_by_condition('xpath', '//div[@class="file-tickets-cmp"]')  # 点击添加标签
        tag = self.add_file_tag()  # 选中标签，添加
        self.click_keyboard('esc')
        self.choose_test_file('img')
        time.sleep(3)
        cur_tag = self.find_by_condition('class', 'ticket-name').get_attribute('innerText').strip()  # 获取当前文件标签
        if cur_tag == tag:  # 判断当前标签是否和选中的标签一致
            logger.info('添加标签成功')
        else:
            logger.error('添加标签失败')
            assert 0
        self.click_by_condition('class', 'delete-box', '删除标签')
        if self.check_condition('class', 'ticket-name'):  # 检测标签元素是否存在
            logger.info('检测到标签，删除失败')
        else:
            logger.info('删除标签成功')

    def change_file_link_by_info(self):
        """修改文件链接"""
        link_url = 'www.baidu.com'
        # 获取添加链接元素
        link_ele = self.finds_by_condition('xpath', '//div[@class="el-collapse-item__content"]//input')[1]
        link_ele.clear()  # 清空输入框
        link_ele.send_keys(link_url)  # 输入url
        time.sleep(1)
        pyautogui.press('Return')
        time.sleep(3)
        cur_link = link_ele.get_attribute('value').strip()  # 获取当前输入框内容
        if cur_link == link_url:
            logger.info('添加链接成功')
        else:
            logger.error('添加链接失败')
            assert 0
        self.click_by_condition('class', 'tolink', '打开链接')
        self.close_another_page()
        self.click_keyboard('esc')
        logger.info('打开链接成功')
        time.sleep(3)

    def create_dir_by_file(self):
        """通过选中文件创建文件夹"""
        self.get_project_file_list()[-1].click()
        self.click_by_text('div', '用所选文件新建文件夹')
        self.click_by_text('div', '确认')
        time.sleep(3)
        if self.check_condition('xpath', '//span[text()="文件夹"]'):  # 新建成功后会出现文件夹文本
            logger.info('新建文件夹成功')
        else:
            logger.error('新建文件夹失败')
            assert 0

    def copy_all_files(self, to_project=''):
        """复制所有文件"""
        self.select_all_file()  # 选中所有文件
        try:
            self.click_by_condition('class', 'moreOpt')
            self.click_by_condition_index('class', 'iconfuzhi_fuzhi', -1, '复制到', 5)
        except:
            self.click_by_condition('class', 'iconfuzhi_fuzhi', '复制到', 5)  # 点击复制到
        self.click_by_condition_index('class', 'tab-item', 0, '项目')  # 点击项目
        self.click_by_condition_index('xpath', f'//div[contains(text(), "{to_project}")]', -1, to_project)  # 点击复制到项目
        self.click_by_text('div', '确定', timeout=2)  # 点击确定
        logger.info('等待十秒，复制完成')
        time.sleep(10)
        # 检测成功文本异常
        # if self.wait_until_text(text='您复制到项目的文件已成功', timeout=30):  # 检测通知
        #     logger.info('检测到复制成功通知')
        # else:
        #     logger.error('未检测到复制成功通知')
        #     assert 0
        file_count = len(self.get_project_file_list())  # 项目内文件数
        self.open_project(to_project)  # 打开被复制项目
        new_count = len(self.get_project_file_list())  # 获取被复制项目内文件数
        if new_count == file_count:  # 对比是否一致
            logger.info('检测到被复制项目文件数相同，复制成功')
        else:
            logger.error('被复制项目和测试项目文件数不一致，复制失败')
            assert 0

    def move_all_files(self, to_project=''):
        """移动所有文件"""
        before_move_count = len(self.get_project_file_list())  # 获取移动前，项目文件数
        self.select_all_file()  # 选中所有文件
        try:
            self.click_by_condition('class', 'moreOpt')
            self.click_by_condition_index('class', 'iconmove', -1, '移动到')  # 点击移动到
        except:
            self.click_by_condition('class', 'iconmove', '移动到')  # 点击移动到
        self.click_by_condition_index('xpath', f'//div[contains(text(), "{to_project}")]', -1)  # 选择移动到项目
        self.click_by_text('div', '确定', timeout=0.5)  # 点击确定
        if self.wait_until_text(text='移动成功', timeout=30):  # 检测移动成功toast
            logger.info('检测到移动成功通知')
        else:
            logger.error('未检测到移动成功通知')
            assert 0
        after_move_count = len(self.get_project_file_list())  # 获取移动后，项目文件数
        self.open_project(to_project)  # 打开被移动项目
        new_count = len(self.get_project_file_list())  # 获取项目文件数
        if new_count == before_move_count and after_move_count == 0:  # 判断移动文件数是否正确，原项目文件是否为0
            logger.info('检测到被移动项目文件数相同，移动成功')
        else:
            logger.error('被移动项目和测试项目文件数不一致，移动失败')
            assert 0

    def download_all_files(self, vip=None):
        """下载所有文件"""
        is_zip = False if vip == 0 else True
        self.select_all_file()  # 选中所有文件
        try:
            self.click_by_condition('class', 'moreOpt')
            self.click_by_condition_index('class', 'iconxiazai_xiazai', -1, '批量下载')
        except:
            self.click_by_condition('class', 'iconxiazai_xiazai', '批量下载')  # 点击下载
        if vip == 0:
            self.close_download_tip()
            self.click_by_img('allow_download', '允许下载多个文件')  # 浏览器授权允许下载多个文件
        time.sleep(10)
        file_count = 1 if is_zip else len(self.get_project_file_list())  # 获取当前项目文件数
        self.check_download(file_count, is_zip=is_zip)

    def check_in_file_detail_view(self):
        """检测是否进入详情页"""
        if self.check_condition('class', 'player-content'):  # 通过检测播放器是否存在判断是否进入详情页
            logger.info('检测到播放器，进入文件详情页成功')
        else:
            logger.error('未检测到播放器，进入文件详情页失败')
            assert 0

    def open_file_settings(self, file_index=0):
        """打开文件设置 file_index--要打开的文件索引"""
        self.click_by_condition_index('xpath', '//*[@id="project-file__content"]//\
                                                        div[@class="el-tooltip more-icon item"]', file_index, '文件设置')

    def set_top(self):
        """置顶"""
        end_file = self.get_project_file_name_list()[-1]
        logger.info(f'文件列表最后一个文件为：{end_file}')
        self.open_file_settings(-1)
        self.click_by_condition_index('xpath', '//div[contains(text(), "置顶")]', -1, '置顶')
        if self.wait_until_text(text='置顶成功'):
            logger.info('检测到「置顶成功」')
            time.sleep(2)
        else:
            logger.error('未检测到「置顶成功」')
            assert 0
        self.check_top(end_file)

    def check_top(self, file_name):
        """检测置顶状态"""
        if self.get_project_file_name_list()[0] == file_name:
            logger.info('检测到第一个文件为置顶文件')
            time.sleep(2)
        else:
            logger.error('第一个文件不是置顶文件')
            assert 0
        if self.check_condition('xpath', '//div[@class="verify-info--wrapper"]/div[text()="TOP"]'):
            logger.info('检测到置顶图标')
        else:
            logger.error('未检测到置顶图标')
            assert 0

    def set_read_status(self, status='待审核'):
        """设置审阅状态"""
        self.open_file_settings()
        self.click_by_condition_index('xpath', '//span[contains(text(), "设置审阅状态")]', -1, '设置审阅状态')
        self.click_by_condition_index('xpath', f'//div[contains(text(), "{status}")]', -1, status)

    def check_read_status(self, status='待审核'):
        """检测审阅状态"""
        if self.check_condition('xpath', f'//div[@class="verify-box"]/span[text()="{status}"]'):
            logger.info('检测到审阅状态图标')
        else:
            logger.error('未检测到审阅状态图标')
            assert 0

    def enter_file_detail_view(self, file_type='img'):
        """进入文件详情页"""
        file_index = self.get_match_file_index(file_type)
        self.click_by_condition_index('xpath', '//*[@id="project-file__content"]//\
                                                div[@class="el-tooltip more-icon item"]', file_index, '文件设置')
        self.click_by_condition_index('xpath', '//div[contains(text(), "查看详情")]', -1, '查看详情')
        time.sleep(5)

    def get_ele_height(self, ele=''):
        """获取元素高度"""
        height = re.findall(r'height: +(\d+.?\d+)px', self.get_ele_style(ele))
        if height:
            return int(eval(height[0]))
        else:
            return 0

    def set_img_fill_height(self):
        """上下撑满"""
        player = self.find_by_condition('class', 'viewer-container')  # 获取播放器元素
        player_height = self.get_ele_height(player)  # 获取播放器高度
        logger.info(f'播放器高度为: {player_height}')
        if player_height == 0:
            logger.error('播放器高度为0，页面异常或播放器控件获取异常！')
            assert 0
        for i in range(3):
            self.click_by_condition('class', 'iconchenggao', '上下撑满')  # 点击上下撑满
            img = self.find_by_condition('class', 'viewer-move')  # 获取图像元素
            img_height = self.get_ele_height(img)  # 获取图像高度
            logger.info(f'图片高度为: {img_height}')
            if abs(player_height - img_height) <= 1:  # 允许图片和播放器有1px误差
                logger.info('上下撑满成功')
                break
        else:
            logger.error('上下撑满失败')
            assert 0

    def set_img_fill_width(self):
        """左右撑满"""
        player = self.find_by_condition('class', 'viewer-container')  # 获取播放器元素
        player_width = self.get_ele_width(player)  # 获取播放器宽度
        logger.info(f'播放器宽度为: {player_width}')
        if player_width == 0:
            logger.error('播放器宽度为0，页面异常或播放器控件获取异常！')
            assert 0
        for i in range(3):
            self.click_by_condition('class', 'iconchengkuan', '左右撑满')  # 点击左右撑满
            img = self.find_by_condition('class', 'viewer-move')  # 获取图像元素
            img_width = self.get_ele_width(img)  # 获取图像宽度
            logger.info(f'图片宽度为: {img_width}')
            if abs(player_width - img_width) <= 1:  # 允许图片和播放器有1px误差
                logger.info('左右撑满成功')
                break
        else:
            logger.error('左右撑满失败')
            assert 0

    def set_img_smaller(self):
        """图片缩小"""
        scale_text = self.find_by_condition('id', 'scale_text').get_attribute('innerText').strip()  # 获取当前比例
        img = self.find_by_condition('class', 'viewer-move')  # 获取图像元素
        img_width, img_height = self.get_ele_width(img), self.get_ele_height(img)  # 获取图像宽、高
        logger.info(f'图片显示比例为：{scale_text}，宽：{img_width}，高：{img_height}')
        self.click_by_condition('id', 'shrinkBtn', '缩小')  # 点击缩小
        cur_scale_text = self.find_by_condition('id', 'scale_text').get_attribute('innerText').strip()  # 获取当前比例
        cur_img_width, cur_img_height = self.get_ele_width(img), self.get_ele_height(img)  # 获取图像宽、高
        logger.info(f'当前图片显示比例为：{cur_scale_text}，宽：{cur_img_width}，高：{cur_img_height}')
        if cur_scale_text < scale_text and cur_img_height < img_height and cur_img_width < img_width:  # 对比判断
            logger.info('缩小成功')
        else:
            logger.error('缩小失败')
            assert 0

    def set_img_larger(self):
        """图片放大"""
        scale_text = self.find_by_condition('id', 'scale_text').get_attribute('innerText').strip()  # 获取当前比例
        img = self.find_by_condition('class', 'viewer-move')  # 获取图像元素
        img_width, img_height = self.get_ele_width(img), self.get_ele_height(img)  # 获取图像宽、高
        logger.info(f'图片显示比例为：{scale_text}，宽：{img_width}，高：{img_height}')
        self.click_by_condition('id', 'magnifyBtn', '放大')  # 点击放大
        cur_scale_text = self.find_by_condition('id', 'scale_text').get_attribute('innerText').strip()  # 获取当前比例
        cur_img_width, cur_img_height = self.get_ele_width(img), self.get_ele_height(img)  # 获取图像宽、高
        logger.info(f'当前图片显示比例为：{cur_scale_text}，宽：{cur_img_width}，高：{cur_img_height}')
        if cur_scale_text > scale_text and cur_img_height > img_height and cur_img_width > img_width:  # 对比判断
            logger.info('放大成功')
        else:
            logger.error('放大失败')
            assert 0

    def control_img_small_map(self, show=True):
        """控制图片小地图打开/关闭"""
        control = '打开' if show else '关闭'  # 根据参数修改话术
        self.click_by_condition('class', 'iconmap', f'{control}画面小地图')  # 点击控制小地图图标
        small_map = self.find_by_condition('class', 'preview-map-container')  # 获取小地图元素
        small_map_style = self.get_ele_style(small_map)  # 获取小地图样式
        if show:
            if not small_map_style:  # 显示时，样式为空
                logger.info(f'小地图{control}成功')
            else:
                logger.error(f'元素样式为：{small_map_style}, 小地图{control}失败')
                assert 0
        else:
            if 'display: none' in small_map_style:  # 隐藏时，display样式为none
                logger.info(f'小地图{control}成功')
            else:
                logger.error(f'元素样式为：{small_map_style}, 小地图{control}失败')
                assert 0

    def open_keyboard_guide(self):
        """显示键盘快捷键"""
        self.click_by_condition_index('class', 'player-ctrl__item--hover', -2, '键盘快捷键')
        keyboard_button = self.find_by_condition('xpath', '//div[contains(text(), "键盘快捷键")]/../../..')  # 获取'键盘快捷键'按钮元素
        keyboard_button_style = self.get_ele_style(keyboard_button)  # 获取'键盘快捷键'按钮样式
        if 'display' in keyboard_button_style:  # 判断按钮是否显示
            logger.error('键盘快捷键元素为隐藏状态')
            assert 0
        keyboard_button.click()  # 按钮按钮
        if self.check_condition('class', 'dialog-container'):  # 检测快捷键对话框是否存在
            logger.info('检测到快捷键对话框，打开成功')
        else:
            logger.error('未检测到快捷键对话框，打开失败')
            assert 0

    def close_keyboard_guide(self):
        """关闭快捷键对话框"""
        self.click_by_condition('class', 'dialog__close', '关闭快捷键对话框')  # 点击关闭对话框
        if self.check_condition('class', 'dialog-container'):  # 检测快捷键对话框是否存在
            logger.error('检测到快捷键对话框，关闭失败')
            assert 0
        else:
            logger.info('未检测到快捷键对话框，关闭成功')

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

    def change_file_in_detail_view(self):
        """文件详情页切换文件"""
        self.click_by_condition('class', 'toggle-icon-wrap', '打开文件列表')  # 点击打开文件列表
        file_list = self.finds_by_condition('xpath', '//div[@class="file-list-content"]/ul/li')  # 获取文件列表
        if len(file_list) == 1:  # 文件数为1 无需测试
            logger.info('项目内文件数为1，跳过测试')
            return True
        # 获取当前文件名，检测是第几个文件
        cur_file_name = self.find_by_condition('class', 'file-item-name').get_attribute('innerText').strip()
        file_name_ele = self.finds_by_condition('class', 'file-name')
        file_name_list = [self.get_text(f) for f in file_name_ele]
        cur_num = file_name_list.index(cur_file_name)
        # 判断下一个文件是向下选还是向上选
        change_num = cur_num + 1 if cur_num < len(file_name_list) - 1 else cur_num - 1
        next_file_name = file_name_list[change_num]
        logger.info(f'下一个文件名为：{next_file_name}, 点击选中')
        file_list[change_num].click()  # 点击第二个文件
        time.sleep(5)
        # 获取当前文件名
        cur_file_name = self.find_by_condition('class', 'file-item-name').get_attribute('innerText').strip()
        if cur_file_name == next_file_name:  # 对比文件名，判断切换文件是否成功
            logger.info('切换文件成功，切回原文件')
            file_list[cur_num].click()
            time.sleep(2)
        else:
            logger.error('切换文件失败')
            self.click_by_condition('class', 'toggle-icon-wrap', '关闭文件列表')  # 再次点击，关闭文件列表
            assert 0
        self.click_by_condition('class', 'toggle-icon-wrap', '关闭文件列表')  # 再次点击关闭文件列表

    def video_player_start(self):
        """点击播放器开关"""
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

    def get_video_player_time(self):
        """获取播放器播放时间"""
        time_ele = self.find_by_condition('class', 'player-ctrl__curTime')
        play_time = self.get_text(time_ele).split('/')[0].strip()
        logger.info(f'当前播放器时间为：{play_time}')
        return play_time

    def get_video_player_duration(self):
        """获取视频总时长"""
        duration_ele = self.find_by_condition('class', 'player-ctrl__duration')
        return self.get_text(duration_ele)[3:]

    @staticmethod
    def get_player_seconds(p_time=''):
        """解析播放器时间为秒数"""
        time_list = p_time.split(':')
        sec = 0
        for i, t in enumerate(time_list):
            sec += int(t) * 60 ** (len(time_list) - i - 1)
        return sec

    def compare_time(self, timeout=3):
        cur_play_time = self.get_video_player_time()
        logger.info(f'等待{timeout}秒后再次检测')
        time.sleep(timeout)
        play_time = self.get_video_player_time()
        return self.get_player_seconds(play_time) - self.get_player_seconds(cur_play_time)

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

    def video_sound_control(self):
        """点击音量控制"""
        self.click_by_condition_index('class', 'player-ctrl__item', 5, '音量控制')

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

    def change_video_time_code_to_normal(self):
        """时间码格式修改--标准"""
        self.click_by_condition('class', 'player-ctrl__curTime')
        self.click_by_condition_index('xpath', '//div[text()="标准"]', -1, '标准')
        player_time = self.get_video_player_time()
        check_list = player_time.split(':')
        if len(check_list) == 2:
            logger.info('时间码格式切换为--标准 成功')
        else:
            logger.error('时间码格式切换为--标准 失败')
            assert 0

    def change_video_time_code_to_fps(self):
        """时间码格式修改--帧"""
        self.click_by_condition('class', 'player-ctrl__curTime')
        self.click_by_condition_index('xpath', '//div[text()="帧"]', -1, '帧')
        player_time = self.get_video_player_time()
        if ':' in player_time:
            logger.error('时间码格式切换为--帧 失败')
            assert 0
        else:
            logger.info('时间码格式切换为--帧 成功')

    def change_video_time_code_to_code(self):
        """时间码格式修改--时间码"""
        self.click_by_condition('class', 'player-ctrl__curTime')
        self.click_by_condition_index('xpath', '//div[text()="时间码"]', -1, '时间码')
        player_time = self.get_video_player_time()
        check_list = player_time.split(':')
        if len(check_list) == 4:
            logger.info('时间码格式切换为--时间码 成功')
        else:
            logger.error('时间码格式切换为--时间码 失败')
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
        self.refresh()
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

    def check_download_icon_status(self, is_gray=True):
        """检测下载交付图标状态"""
        icon_ele = self.find_by_condition('class', 'download-control')
        if 'is-grey' in icon_ele.get_attribute('class'):
            logger.info('检测到下载交付图标为置灰状态')
            if is_gray:
                return True
            else:
                assert 0
        else:
            logger.info('检测到下载交付图标非置灰状态')
            if is_gray:
                assert 0
            else:
                return True

    def check_cover_icon_status(self, is_gray=True):
        """检测设置封面图标状态"""
        icon_ele = self.find_by_condition('class', 'icontupian_tupian')
        if 'is-grey' in icon_ele.get_attribute('class'):
            logger.info('检测到设置封面图标为置灰状态')
            if is_gray:
                return True
            else:
                assert 0
        else:
            logger.info('检测到设置封面图标非置灰状态')
            if is_gray:
                assert 0
            else:
                return True

    def check_fangluping_icon_status(self, is_gray=True):
        """检测设置封面图标状态"""
        icon_ele = self.find_by_condition('class', 'iconic_fangluping')
        if 'is-grey' in icon_ele.get_attribute('class'):
            logger.info('检测到防录屏图标为置灰状态')
            if is_gray:
                return True
            else:
                assert 0
        else:
            logger.info('检测到防录屏图标非置灰状态')
            if is_gray:
                assert 0
            else:
                return True

    def add_discussion(self, info='这是一条评论', file='img.jpg'):
        """添加审批意见"""
        self.click_by_text(text='审评意见')
        input_ele = self.find_by_condition('id', 'input-area')
        input_ele.clear()
        input_ele.send_keys(info)
        self.add_file_in_comment(file)
        self.click_by_text(text='发送', timeout=5)

    def check_discussion(self, info='这是一条评论', file=False):
        first_dis_ele = self.finds_by_condition('xpath', '//span[@class="comment-item-content-text"]/span')[0]
        first_dis = self.get_text(first_dis_ele)
        if first_dis == info:
            logger.info('添加意见成功')
        else:
            logger.error('添加意见失败')
            assert 0
        if file:
            if self.check_condition('class', 'upload-img'):
                logger.info('评论中检测到上传附件')
            else:
                logger.error('评论中未检测到上传附件')
                assert 0

    def check_share_version_status(self):
        """检测分享版本选中状态"""
        self.click_by_text(ele_type='div', text='审阅分享')
        self.click_by_text(ele_type='p', text='分享链接', timeout=5)
        self.click_by_condition('xpath', '//span[contains(text(), "分享链接")]/../../i')
        e_class = self.find_by_condition('class', 'version-opt').get_attribute('class')
        self.click_by_condition('xpath', '//div[@class="dialog-header-content"]/i')
        if 'disabled' in e_class:
            logger.info('分享版本选择按钮无法选中，验证通过')
            return True
        else:
            logger.error('分享版本按钮非disable状态，验证失败')
            assert 0

    def choose_share_version(self, version=None):
        """选择分享版本"""
        if not version or not self.check_text(text='分享版本'):
            return True
        version = version.upper()
        self.click_by_condition('class', 'version-opt', '选择分享版本')
        if version == 'ALL':
            self.click_by_text(ele_type='span', text='全部版本')
        else:
            self.click_by_text(ele_type='span', text='单个版本')
            self.click_by_text(ele_type='span', text=version)
        self.click_by_condition('xpath', '//span[contains(text(), "选择分享版本")]/../../i')
        cur_version = self.get_text(self.find_by_condition('xpath', '//div[@class="version-opt"]/span'))
        logger.info(f'当前分享版本为：{cur_version}')
        if (version == 'ALL' and cur_version == '全部版本') or version == cur_version:
            logger.info('版本选择成功！')
            return True
        else:
            logger.error('版本选择异常！')
            assert 0

    def share(self, version=None, detail_view=False):
        """审阅分享"""
        share_ele = 'div' if detail_view else 'button'
        self.click_by_text(ele_type=share_ele, text='审阅分享')
        if self.check_text(text='创建审阅分享'):
            logger.info('检测到分享弹窗')
        else:
            logger.error('未检测到分享弹窗')
            assert 0
        self.choose_share_version(version)
        ele = self.find_by_condition('xpath', f'//p[text()="允许下载和转存"]/../../span/span/div')
        if 'is-checked' not in ele.get_attribute('class'):
            logger.info(f'下载权限未开启，点击开启')
            ele.click()
            time.sleep(2)
        self.click_by_text(ele_type='p', text='分享链接', timeout=5)
        if self.check_text(ele_type='span', text='分享链接'):
            logger.info('检测到分享链接')
        else:
            logger.error('未检测到分享链接')
            self.close_share_dialog()
            assert 0
        self.click_by_condition('class', 'copy-btn', '复制', timeout=0.5)
        if self.wait_until_text(text='复制成功'):
            logger.info('检测到「复制成功」')
        else:
            logger.error('未检测到「复制成功」')
            self.close_share_dialog()
            assert 0
        link = re.findall(r'链接：(.*?)\n', self.get_copy_text())
        if link:
            logger.info(f'分享链接为：{link[0]}')
            self.close_share_dialog()
            return link[0]
        else:
            logger.error('未提取到链接')
            self.close_share_dialog()
            assert 0

    def get_file_list_in_share_page(self):
        """获取分享落地页文件名列表"""
        name_ele_list = self.finds_by_condition('xpath', '//div[@class="subInfo-title"]/span')
        name_list = [self.get_text(e) for e in name_ele_list]
        return name_list

    def collect(self):
        """分享落地页-收藏"""
        self.click_by_condition('class', 'collect', '收藏', 0)
        if self.wait_until_text(text='不能收藏自己的链接'):
            logger.info('检测到「不能收藏自己的链接」')
        elif self.check_text(text='收藏成功'):
            logger.info('检测到收藏成功')
        else:
            logger.error('收藏功能异常')
            assert 0

    def download_in_share_page(self):
        """分享落地页下载"""
        self.click_by_condition('class', 'download', '下载')
        self.click_by_condition_index('class', 'file-card-wrapper', 0, '选择文件')
        self.click_by_condition('class', 'download', '下载')
        # if self.check_text(text='确认下载'):
        #     self.click_by_text(text='确认下载')
        self.click_by_text(ele_type='button', text='取消')
        logger.info('等待10秒下载文件')
        time.sleep(10)
        if len(os.listdir(self.download_path)):
            logger.info('检测到下载文件，下载成功')
            shutil.rmtree(self.download_path)  # 清空下载文件夹
            os.mkdir(self.download_path)
        else:
            logger.error('未检测到下载文件')
            assert 0

    def move(self):
        """转存"""
        self.switch_to_main_page()
        file_count = len(self.get_project_file_list())
        logger.info(f'转存前文件数为：{file_count}')
        self.switch_to_another_page()
        self.click_by_condition('class', 'move', '转存')
        self.click_by_condition_index('class', 'file-card-wrapper', 0, '选择文件')
        self.click_by_condition('class', 'move', '转存')
        self.click_by_text(text=parse.project_name)
        self.click_by_text(text='确定')
        logger.info('等待10秒转存')
        time.sleep(10)
        self.switch_to_main_page()
        self.refresh()
        self.open_project()
        cur_file_count = len(self.get_project_file_list())
        logger.info(f'转存后文件数为：{cur_file_count}')
        self.switch_to_another_page()
        if cur_file_count - file_count == 1:
            logger.info('检测到项目文件数增加，转存成功')
        else:
            logger.error('转存失败')
            assert 0

    def check_share_download_permission(self, download=False):
        """检测分享落地页下载权限"""
        ele = self.find_by_condition('class', 'download')
        if 'is-grey' in ele.get_attribute('class'):
            logger.info('下载按钮置灰')
            if download:
                assert 0
        else:
            logger.info('下载按钮未置灰')
            if not download:
                assert 0

    def check_share_move_permission(self, move=False):
        """检测分享落地页下载权限"""
        ele = self.find_by_condition('class', 'move')
        if 'is-grey' in ele.get_attribute('class'):
            logger.info('转存按钮置灰')
            if move:
                assert 0
        else:
            logger.info('转存按钮未置灰')
            if not move:
                assert 0

    def enter_share_file_detail(self):
        """进入分享文件详情页"""
        logger.info('双击文件进入详情页')
        for i in range(5):
            self.click_by_condition_index('class', 'file-thumbnail', 0, timeout=0.1)
            self.click_by_condition_index('class', 'file-thumbnail', 0)
            if self.check_text(text='发送'):
                logger.info('已进入详情页')
                break
            else:
                logger.info('未进入详情页，重试')
        else:
            logger.error('进入详情页失败')
            assert 0

    def check_share_comment_permission(self, comment=False):
        """分享评论权限验证"""
        self.click_by_text(text='发送')
        if self.check_text(text='您无权进行此操作'):
            logger.info('无评论权限')
            self.click_by_condition('class', 'btnCommon', '好的')
            if comment:
                assert 0
        else:
            logger.info('可评论')
            if not comment:
                assert 0

    def close_project_permission(self, *args, role='成员'):
        """关闭身份权限"""
        if parse.is_company.lower() == 'true':
            self.close_project_setting()
            pytest.skip('企业版不支持修改身份权限')
        role_dict = {'成员': 'member',
                     '管理员': 'admin'}
        self.click_by_condition('class', 'down-box', '身份权限设置')
        for s in args:
            path = f'//p[text()="{s}"]/../..//div[@class="{role_dict[role]}-select"]/span[1]'
            ele = self.find_by_condition('xpath', path)
            if 'is_checked' in ele.get_attribute('class'):
                logger.info(f'{s} 权限为开启状态，点击关闭')
                try:
                    ele.click()
                except ex.ElementClickInterceptedException as e:
                    logger.error('元素点击异常')
                    self.close_project_setting()
                    assert 0
                if self.wait_until_text(text='操作成功'):
                    logger.info(f'{s} 权限配置成功')
                    time.sleep(2)
                else:
                    logger.error(f'{s} 权限配置异常')
                    self.close_project_setting()
                    assert 0
            else:
                logger.info(f'{s} 权限为关闭状态')
        self.close_project_setting()

    def check_change_info_permission_close(self):
        """检测自定义信息权限关闭"""
        try:
            self.click_by_condition_index('xpath', '//div[@class="rate-icon-wrap"]/span', 0, '自定义信息', 0)
            logger.error('编辑成功')
            assert 0
        except ex.ElementClickInterceptedException as e:
            logger.info('该元素不可点击')

    def check_invite_permission_close(self):
        """检测邀请权限关闭"""
        if self.check_condition('class', 'add-btn'):
            logger.error('检测到邀请按钮')
            assert 0
        else:
            logger.info('未检测到邀请按钮')

    def check_delete_permission_close(self):
        """检测删除权限关闭"""
        if self.check_condition('class', 'iconshanchu'):
            logger.error('检测到删除按钮')
            assert 0
        else:
            logger.info('未检测到删除按钮')

    def check_copy_permission_close(self):
        """检测复制权限关闭"""
        xpath = '//div[@class="share-control--wrapper"]//span[@class="iconfont iconshanchu operation-icon"]'
        if self.check_condition('xpath', xpath):
            logger.error('检测到复制按钮')
            assert 0
        else:
            logger.info('未检测到复制按钮')

    def check_download_permission_close(self):
        """检测下载权限关闭"""
        if self.check_condition('class', 'iconjiaofu_download'):
            logger.error('检测到下载按钮')
            assert 0
        else:
            logger.info('未检测到下载按钮')

    def check_share_permission_close(self):
        """检测分享权限关闭"""
        if self.check_text(ele_type='button', text='审阅分享'):
            logger.error('检测到分享按钮')
            assert 0
        else:
            logger.info('未检测到分享按钮')

    def create_receive_link(self):
        """创建收集链接"""
        self.click_by_condition('xpath', '//button[contains(text(), "上传/新建")]', '上传/新建')
        self.click_by_text('div', '收集文件')
        if self.check_text(ele_type='span', text='创建收集'):
            logger.info('检测到创建收集弹窗')
        else:
            logger.error('未检测到创建收集弹窗')
            assert 0
        receive_name_ele = self.find_by_condition('class', 'el-input__inner')
        receive_name_ele.clear()
        receive_name_ele.send_keys(parse.receive_dir)
        self.click_by_condition('class', 'confirm', '创建', 5)
        if self.check_condition('class', 'link-text'):
            self.click_by_condition('class', 'copy-btn', '复制链接')
            receive_link = re.findall(r'(.*?) 打开', self.get_copy_text())[0]
            logger.info(f'检测到收集链接：{receive_link}')
            self.close_receive_dialog()
            return receive_link
        else:
            logger.error('未检测到收集链接')
            self.click_by_condition('class', 'cancel', '取消')
            assert 0

    def upload_file_by_receive_link(self, file='img.jpg'):
        """通过收集链接上传文件"""
        self.click_by_condition('class', 'iconshangchuan_shangchuan', '选择文件')
        # self.click_by_condition('class', 'upload-file--wrapper', '上传文件')
        self.choose_file_to_upload(file)
        if self.wait_until_text(text=file):
            logger.info('检测到文件名')
        else:
            logger.error('未检测到文件名')
            assert 0
        self.click_by_text(text='发送给对方')
        self.wait_receive_upload()

    def check_receive(self):
        """验证收集"""
        self.choose_test_file(file_name=parse.receive_dir)
        if eval(self.get_dir_file_count()) == 1:
            logger.info('收集成功')
        else:
            logger.error('收集失败')
            assert 0

    def import_url(self, url='https://www.baidu.com/'):
        """导入链接文件"""
        self.click_by_condition('xpath', '//button[contains(text(), "上传/新建")]', '上传/新建')
        self.click_by_text('span', '网页地址')
        url_input = self.finds_by_condition('class', 'el-input__inner')[0]
        title_input = self.finds_by_condition('class', 'el-input__inner')[1]
        url_input.clear()
        url_input.send_keys(url)
        self.click_by_text(text='导入网页地址')
        title = title_input.get_attribute('value').strip()
        if not title:
            logger.error('未获取到链接标题')
            assert 0
        logger.info(f'链接标题为：{title}')
        self.click_by_text(ele_type='span', text='确定')
        if self.wait_until_text(text='导入成功'):
            logger.info('网页导入成功')
            self.close_upload_page()
            time.sleep(5)
        else:
            logger.error('网页导入失败')
            assert 0

    def check_web_file_download_button(self):
        """检测链接文件下载按钮"""
        self.choose_test_file(file_type='web')
        try:
            self.click_by_condition('class', 'moreOpt')
            self.click_by_condition_index('class', 'iconxiazai_xiazai', -1, '下载', 0)
        except:
            self.click_by_condition('class', 'iconxiazai_xiazai', '下载', 0)  # 点击下载
        if self.wait_until_text(text='链接文件暂不支持下载'):
            logger.info('检测到「链接文件暂不支持下载」')
        else:
            logger.error('未检测到「链接文件暂不支持下载」')
            assert 0

    def check_download_web_and_other_file(self):
        """检测下载网页和其他类型文件"""
        self.choose_test_file(file_type='web')
        self.choose_other_file(file_type='img')
        try:
            self.click_by_condition('class', 'moreOpt')
            self.click_by_condition_index('class', 'iconxiazai_xiazai', -1, '批量下载')
        except:
            self.click_by_condition('class', 'iconxiazai_xiazai', '批量下载')  # 点击下载
        # if not self.is_company():
        #     self.click_by_text('div', '确认下载')  # 二次确认
        time.sleep(10)
        self.check_download(1)

    def add_file_in_comment(self, file='img.jpg'):
        """审评意见添加附件"""
        if not file:
            return True
        for i in range(5):
            self.click_by_condition('class', 'iconfujian', '添加附件')
            if self.choose_file_to_upload(file):
                break
        time.sleep(5)
        icon = self.find_by_condition('class', 'fujian-wrapper')
        if 'isHasImg' in icon.get_attribute('class'):
            logger.info('检测到附件添加成功')
        else:
            logger.error('附件添加失败')
            assert 0

    def check_many_version(self, many=True):
        """检测多版本图标"""
        if self.check_condition('xpath', '//div[@class="subscript"]/span[text()="V2"]'):
            logger.info('检测到多版本图标--v2')
            if not many:
                assert 0
        else:
            logger.info('未检测到多版本图标--v2')
            if many:
                assert 0

    def add_version(self, file_type='img', file_name='img.jpg'):
        """添加版本"""
        for i in range(5):
            self.open_file_settings(self.get_match_file_index(file_type))
            self.click_by_condition_index('xpath', '//span[contains(text(), "版本管理")]', -1, '版本管理')
            self.click_by_condition_index('xpath', '//div[contains(text(), "上传版本")]', -1, '上传版本')
            if self.choose_file_to_upload(file_name):
                break
        self.wait_upload()
        self.check_many_version()

    def compare_version(self):
        """版本对比"""
        self.click_by_condition('class', 'version-control__panel', '版本管理')
        self.click_by_condition('class', 'compare-btn', '对比', timeout=3)
        if self.check_condition('class', 'video-player-content'):
            logger.info('检测到对比播放器，已进入对比页面')
        else:
            logger.error('未检测到对比播放器')
            assert 0
        self.click_by_condition_index('xpath', '//div[@class="control-item"]/../div[2]/div/div/div', 0, '播放', 3)
        self.click_by_condition_index('xpath', '//div[@class="control-item"]/../div[2]/div/div/div', 0, '暂停')
        player_time = self.finds_by_condition('xpath', '//span[@class="player-ctrl__curTime"]')[0]
        if '00:00' in self.get_text(player_time):
            logger.error('播放器时间未改变')
            self.click_by_condition('class', 'iconfanhui_fanhui', '返回', 5)
            assert 0
        else:
            logger.info('播放成功')
        self.click_by_condition('class', 'iconfanhui_fanhui', '返回', 5)

    def remove_version(self):
        """删除版本"""
        self.click_by_condition('class', 'version-control__panel', '版本管理')
        self.click_by_condition('class', 'version-btn', '管理')
        self.click_by_condition_index('xpath', '//div[@class="version-list--wrapper"]//i', 0, '移除版本')
        self.click_by_condition_index('xpath', '//div[text()="解除单个版本"]', -1, '解除单个版本')
        if self.wait_until_text(text='你已解除全部版本'):
            logger.info('检测到「你已解除全部版本」，解除版本成功')
        else:
            logger.error('未检测到「你已解除全部版本」，解除版本失败')
            assert 0

    def open_task_view(self):
        """打开任务看板"""
        if not self.is_company():
            pytest.skip('个人版无任务看板，无需测试')
        self.click_by_condition('xpath', '//div[@class="file-content-header"]//div[contains(text(), "任务看板")]',
                                '任务看板')

    def add_task_menu(self, menu='清单-新增'):
        """新增任务清单"""
        if not self.is_company():
            pytest.skip('个人版无任务看板，无需测试')
        self.click_by_condition('class', 'add-wrapper', '新增任务清单')
        name_ele = self.find_by_condition('class', 'set-name-input')
        name_ele.clear()
        name_ele.send_keys(menu)
        time.sleep(1)
        pyautogui.press('enter')
        if self.wait_until_text(text='创建清单成功'):
            logger.info('创建清单成功')
        else:
            logger.error('创建清单失败')
            assert 0

    def add_task(self, menu='清单-新增', title='任务-新增'):
        """新增任务"""
        if not self.is_company():
            pytest.skip('个人版无任务看板，无需测试')
        self.click_by_condition('xpath',
                                f'//span[text()="{menu}"]/../../..//div[@class="add-task-card iconfont iconjiahao_jiahao"]')
        title_ele = self.find_by_condition('class', 'create-card-textarea')
        title_ele.clear()
        title_ele.send_keys(title)
        time.sleep(1)
        pyautogui.press('enter')
        if self.wait_until_text(text='创建任务成功'):
            logger.info('创建任务成功')
        else:
            logger.error('创建任务失败')
            assert 0

    def open_task_detail(self, title='任务-新增'):
        """打开任务详情"""
        if not self.is_company():
            pytest.skip('个人版无任务看板，无需测试')
        self.click_by_text(ele_type='span', text=title, fuzzy=False)
        if self.check_condition('class', 'mission-dialog'):
            logger.info('检测到任务详情对话框')
            self.close_task_detail()
        else:
            logger.error('未检测到任务详情对话框')
            assert 0

    def close_task_detail(self):
        """关闭任务详情对话框"""
        self.click_by_condition('xpath', '//div[@class="mission-dialog-header"]/i', '关闭任务详情')

    def delete_task_menu(self, menu='清单-新增'):
        """删除任务清单"""
        if not self.is_company():
            pytest.skip('个人版无任务看板，无需测试')
        self.click_by_condition('xpath', f'//span[text()="{menu}"]/../..//div[@class="more-icon"]', '更多设置')
        self.click_by_condition_index('xpath', '//div[@class="more-item-content"]/div[contains(text(), "删除")]', -1, '删除')
        self.click_by_condition('xpath', '//div[@class="space-round"]//div[text()="删除 "]', '删除')
        if self.wait_until_text(text='删除清单成功'):
            logger.info('删除清单成功')
        else:
            logger.error('删除清单失败')
            assert 0
