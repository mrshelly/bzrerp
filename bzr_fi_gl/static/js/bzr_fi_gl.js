/*--------------------------------------------------------------------------------------------------------------------
* 开阖ERP采用AGPL-3协议，版权(CopyRight)归以下代码提交者所有
*
* 2013    开阖软件 Jeff Wang,OpenERPJeff       (jeff@osbzr.com)            初始版本
* 2013       buke                              (wangbuke@gmail.com)        Add session_id to context.bzr_menu_click
 *-----------------------------------------------------------------------------------------------------------------*/




openerp.bzr_fi_gl = function(instance) {
    instance.web.Menu =  instance.web.Menu.extend({
        open_menu: function (id) {
            instance.session.user_context.bzr_menu_click = '' + instance.session.session_id + id + $.now();
            return this._super(id);
        },
    });
};


