# -*- coding: utf-8 -*-
"""
    rstblog.modules.analytics
    ~~~~~~~~~~~~~~~~~~~~~~

    Implements Google Analytics element if asked for.
    
    To use this, include ``analytics`` in the list of modules in your ``config.yml`` file,
    and add a configuration variable to match your settings : ``analytics.id`` 
    
    To prevent analytics on a particular page, set ``analytics = no`` in the page's YAML preamble.

    :copyright: (c) 2013 by Marcin Wielgoszewski.
    :license: BSD, see LICENSE for more details.
"""
import jinja2

@jinja2.contextfunction
def get_analytics(context):

    analytics_id = context['config'].get('analytics_id',

        # fall back to analytics.id from config.yml
        context['builder'].config.root_get('modules.analytics.id', 'YOUR-ANALYTICS-ID'))

    analytics_url = "// _gaq.push(['_setDomainName', '']);"

    if context['builder'].config.root_get('modules.analytics.url', None):
        analytics_url = "_gaq.push(['_setDomainName', '%s']);" % (
            context['builder'].config.root_get('modules.analytics.url'),)

    analytics_txt = """
<script type="text/javascript">
    var _gaq = _gaq || [];
    _gaq.push(['_setAccount', '%s']);
    %s
    _gaq.push(['_trackPageview']);

    (function() {
        var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
        ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
        var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
    })();
</script>
""" % (analytics_id, analytics_url, )

    if not context['config'].get('analytics', True):
        analytics_txt = ''

    return jinja2.Markup(analytics_txt.encode('utf-8'))


def setup(builder):
    builder.jinja_env.globals['get_analytics'] = get_analytics
