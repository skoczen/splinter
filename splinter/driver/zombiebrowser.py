from zombie import Browser
from splinter.element_list import ElementList
from splinter.driver import DriverAPI, ElementAPI
from splinter.driver.webdriver import BaseWebDriver
from splinter.cookie_manager import CookieManagerAPI


class ZombieElement(ElementAPI):
    """
    Basic element API class.

    Any element in the page can be represented as an instance of ``ElementAPI``.

    Once you have an instance, you can easily access its attributes like a ``dict``:

        >>> element = browser.find_by_id("link-logo").first
        >>> assert element['href'] == 'http://splinter.cobrateam.info'

    You can also interact with the instance using the methods and properties listed below.
    """

    def _get_value(self):
        raise NotImplementedError

    def _set_value(self, value):
        raise NotImplementedError

    #: Value of the element, usually a form element
    value = property(_get_value, _set_value)

    def click(self):
        """
        Clicks in the element.
        """
        raise NotImplementedError

    def check(self):
        """
        Checks the element, if it's "checkable" (e.g.: a checkbox).

        If the element is already checked, this method does nothing. For unchecking
        elements, take a loot in the :meth:`uncheck <ElementAPI.uncheck>` method.
        """
        raise NotImplementedError

    def uncheck(self):
        """
        Unchecks the element, if it's "checkable" (e.g.: a checkbox).

        If the element is already unchecked, this method does nothing. For checking
        elements, take a loot in the :meth:`check <ElementAPI.check>` method.
        """
        raise NotImplementedError

    @property
    def checked(self):
        """
        Boolean property that says if the element is checked or not.

        Example:

            >>> element.check()
            >>> assert element.checked
            >>> element.uncheck()
            >>> assert not element.checked
        """
        raise NotImplementedError

    @property
    def visible(self):
        """
        Boolean property that says if the element is visible or hidden in the current page.
        """
        raise NotImplementedError

    def mouse_over(self):
        """
        Puts the mouse over the element.
        """
        raise NotImplementedError

    def mouse_out(self):
        """
        Moves the mouse away from the element.
        """
        raise NotImplementedError

    def __getitem__(self, attribute):
        print "Getting"
        raise NotImplementedError


class ZombieElementList(ElementList):
    pass


class ZombieTestBrowser(DriverAPI):
    """
    Zombie.js driver class.
    """
    driver_name = "zombiejs"

    def __init__(self):
        self._browser = Browser()
        self.element_class = ZombieElement
        # print self._browser.client.wait('cookies', None, None)
        # print self._browser.client.json('cookies()')
        # self._cookie_manager = CookieManager(self._browser.cookies().all())
        self._last_urls = []

    def _element_list_from_list(self, element_list):
        print "element_list", element_list
        zel = ZombieElementList([])
        elist = []
        for e in element_list:
            try:
                print e
                print ZombieElement(e, self)
                print ZombieElement(e, self).__dict__
                elist.append(ZombieElement(e, self))
            except:
                from traceback import print_exc
                print_exc()

        print "zel", zel
        print "elist", elist
        return ZombieElementList(elist)
        return zel
        return ZombieElementList([ZombieElement(ele, self) for ele in element_list])

    @property
    def title(self):
        return self._browser.text("title")

    @property
    def html(self):
        return self._browser.html()

    @property
    def url(self):
        return self._browser.location

    def visit(self, url):
        self._browser.visit(url)

    def back(self):
        self._last_urls.insert(0, self.url)
        self._browser.back()

    def forward(self):
        try:
            self.visit(self._last_urls.pop())
        except IndexError:
            pass

    def reload(self):
        self._browser.reload()

    def get_alert(self):
        """
        Changes the context for working with alerts and prompts.

        For more details, check the :doc:`docs about iframes, alerts and prompts </iframes-and-alerts>`
        """
        raise NotImplementedError

    def get_iframe(self, id):
        self._browser.windowName = id

    def execute_script(self, script):
        self._browser.evaluate(script)

    def evaluate_script(self, script):
        return self._browser.evaluate(script)

    def find_by_css(self, css_selector, context=None):
        print "context", context
        if context:
            print context.__dict__
            print type(context)
        return self._element_list_from_list(self._browser.queryAll(css_selector, context))

    def find_by_xpath(self, xpath):
        return self._element_list_from_list([self._browser.xpath(xpath)])

    def find_by_name(self, name):
        return self.find_by_css("[name=\"%s\"]" % name)

    def find_by_id(self, id):
        return self.find_by_css("#%s" % id)

    def find_by_value(self, value):
        return self.find_by_css("[value=\"%s\"]" % value.replace('"', '\"'))

    def find_by_tag(self, tag):
        return self.find_by_css(tag)

    def find_link_by_href(self, href):
        return self.find_by_css("[href=\"%s\"]" % href)

    def find_link_by_partial_href(self, partial_href):
        return self.find_by_css("[href*=\"%s\"]" % partial_href)

    def find_link_by_text(self, text):
        # TODO: this isn't correct.
        return self.find_by_css("a:contains(\"%s\")" % text.replace('"', '\"'))

    def find_link_by_partial_text(self, partial_text):
        return self.find_by_css("a:contains(\"%s\")" % partial_text.replace('"', '\"'))

    def find_option_by_value(self, value):
        return self.find_by_css("option[value=\"%s\"]" % value.replace('"', '\"'))

    def find_option_by_text(self, text):
        # TODO: this is broken
        return self.find_by_css("option[value=\"%s\"]" % text.replace('"', '\"'))

    def is_text_present(self, text, wait_time=None):
        return text in self._browser.document

    def type(self, name, value, slowly=False):
        """
        Types the ``value`` in the field identified by ``name``.

        It's useful to test javascript events like keyPress, keyUp, keyDown, etc.
        """
        raise NotImplementedError

    def fill(self, name, value):
        return self._browser.fill(name, value)

    def choose(self, name, value):
        return self._browser.choose(name)

    def check(self, name):
        return self._browser.check(name)

    def uncheck(self, name):
        return self._browser.uncheck(name)

    def select(self, name, value):
        return self._browser.select(name, value)

        raise NotImplementedError

    def click_link_by_href(self, href):
        return self._browser.clickLink("[href=\"%s\"]" % href)

    def click_link_by_partial_href(self, partial_href):
        return self._browser.clickLink("[href*=\"%s\"]" % partial_href)

    def click_link_by_text(self, text):
        """
        Clicks in a link by its ``text``.
        """
        return self.find_link_by_text(text).first.click()

    def click_link_by_partial_text(self, partial_text):
        """
        Clicks in a link by partial content of its text.
        """
        return self.find_link_by_partial_text(partial_text).first.click()

    def within(self, context):
        return ElementList([], context, self)

    def quit(self):
        """
        Quits the browser, closing its windows (if it has one).

        After quit the browser, you can't use it anymore.
        """
        pass

    def is_element_present_by_css(self, css_selector, wait_time=None):
        return len(self.find_by_css(css_selector)) > 0

    def is_element_not_present_by_css(self, css_selector, wait_time=None):
        return len(self.find_by_css(css_selector)) == 0

    def is_element_present_by_xpath(self, xpath, wait_time=None):
        return len(self.find_by_xpath(xpath)) > 0

    def is_element_not_present_by_xpath(self, xpath, wait_time=None):
        return len(self.find_by_xpath(xpath)) == 0

    def is_element_present_by_tag(self, tag, wait_time=None):
        return len(self.find_by_tag(tag)) > 0

    def is_element_not_present_by_tag(self, tag, wait_time=None):
        return len(self.find_by_tag(tag)) == 0

    def is_element_present_by_name(self, name, wait_time=None):
        return len(self.find_by_name(name)) > 0

    def is_element_not_present_by_name(self, name, wait_time=None):
        return len(self.find_by_name(name)) == 0

    def is_element_present_by_value(self, value, wait_time=None):
        return len(self.find_by_value(value)) > 0

    def is_element_not_present_by_value(self, value, wait_time=None):
        return len(self.find_by_value(value)) == 0

    def is_element_present_by_id(self, id, wait_time=None):
        return len(self.find_by_id(id)) > 0

    def is_element_not_present_by_id(self, id, wait_time=None):
        return len(self.find_by_id(id)) == 0

    @property
    def cookies(self):
        """
        A :class:`CookieManager <splinter.cookie_manager.CookieManagerAPI>` instance.

        For more details, check the :doc:`cookies manipulation section </cookies>`.
        """
        raise NotImplementedError


# from zombie import Browser
# from splinter.element_list import ElementList
# from splinter.driver import DriverAPI, ElementAPI
# from splinter.cookie_manager import CookieManagerAPI

# import mimetypes
# import lxml.html


# class CookieManager(CookieManagerAPI):

#     def __init__(self, browser_cookies):
#         self._cookies = browser_cookies

#     def add(self, cookies):
#         for key, value in cookies.items():
#             self._cookies[key] = value

#     def delete(self, *cookies):
#         if cookies:
#             for cookie in cookies:
#                 try:
#                     del self._cookies[cookie]
#                 except KeyError:
#                     pass
#         else:
#             self._cookies.clearAll()

#     def __getitem__(self, item):
#         return self._cookies[item]

#     def __eq__(self, other_object):
#         if isinstance(other_object, dict):
#             return dict(self._cookies) == other_object


# class ZombieTestBrowser(DriverAPI):

#     driver_name = "zombiejs"

#     def __init__(self):
#         self._browser = Browser()
#         # print self._browser.client.wait('cookies', None, None)
#         # print self._browser.client.json('cookies()')
#         # self._cookie_manager = CookieManager(self._browser.cookies().all())
#         self._last_urls = []

#     def visit(self, url):
#         self._browser.visit(url)

#     def back(self):
#         self._last_urls.insert(0, self.url)
#         self._browser.back()

#     def forward(self):
#         try:
#             self.visit(self._last_urls.pop())
#         except IndexError:
#             pass

#     def reload(self):
#         self._browser.reload()

#     def quit(self):
#         pass

#     @property
#     def title(self):
#         return self._browser.title()

#     @property
#     def html(self):
#         return self._browser.html()

#     @property
#     def url(self):
#         return self._browser.location

#     def find_option_by_value(self, value):
#         return self._browser.query("option[value=\"%s\"]" % value)

#     def find_option_by_text(self, text):
#         html = lxml.html.fromstring(self.html)
#         element = html.xpath('//option[normalize-space(text())="%s"]' % text)[0]
#         control = self._browser.getControl(element.text)
#         return ElementList([ZombieTestBrowserOptionElement(control, self)], find_by="text", query=text)

#     def find_by_css(self, selector, context=None):
#         return [ZombieTestBrowserElement(z) for z in self._browser.query(selector, context)]

#     def find_by_xpath(self, xpath, original_find=None, original_selector=None):
#         html = lxml.html.fromstring(self.html)

#         elements = []

#         for xpath_element in html.xpath(xpath):
#             if self._element_is_link(xpath_element):
#                 return self.find_link_by_text(xpath_element.text)
#             elif self._element_is_control(xpath_element):
#                 return self.find_by_name(xpath_element.name)
#             else:
#                 elements.append(xpath_element)

#         find_by = original_find or "xpath"
#         query = original_selector or xpath

#         return ElementList([ZombieTestBrowserElement(element, self) for element in elements], find_by=find_by, query=query)

#     def find_by_tag(self, tag):
#         return self._browser.query(tag)

#     def find_by_value(self, value):
#         return self.find_by_css("[value=\"%s\"]" % value)

#     def find_by_id(self, id_value):
#         return self.find_by_css("#%s" % id_value)

#     def find_by_name(self, name):
#         return self.find_by_css("[name=\"%s\"]" % name)

#     def find_link_by_text(self, text):
#         return self._find_links_by_xpath("//a[text()='%s']" % text)

#     def find_link_by_href(self, href):
#         return self._find_links_by_xpath("//a[@href='%s']" % href)

#     def find_link_by_partial_href(self, partial_href):
#         return self._find_links_by_xpath("//a[contains(@href, '%s')]" % partial_href)

#     def find_link_by_partial_text(self, partial_text):
#         return self._find_links_by_xpath("//a[contains(text(), '%s')]" % partial_text)

#     def fill(self, name, value):
#         self._browser.fill(name, value)

#     def choose(self, name, value):
#         self._browser.select(name, value)

#     def check(self, name):
#         self._browser.check(name)

#     def uncheck(self, name):
#         self._browser.uncheck(name)

#     def attach_file(self, name, file_path):
#         self._browser.attach(name, file_path)

#     def _find_links_by_xpath(self, xpath):
#         html = lxml.html.fromstring(self.html)
#         links = html.xpath(xpath)
#         return ElementList([ZombieTestBrowserLinkElement(link, self) for link in links], find_by="xpath", query=xpath)

#     def select(self, name, value):
#         self.find_by_name(name).first._control.value = [value]

#     def _element_is_link(self, element):
#         return element.tag == 'a'

#     def _element_is_control(self, element):
#         return hasattr(element, 'type')

#     @property
#     def cookies(self):
#         return self._cookie_manager


class ZombieTestBrowserElement(ElementAPI):

    def __init__(self, element, parent):
        self._element = element
        self.parent = parent

    def __getitem__(self, attr):
        return self._element.attrib[attr]

    def find_by_css(self, selector):
        elements = self._element.cssselect(selector)
        return ElementList([element for element in self._browser.query(selector, elements)])

    def find_by_xpath(self, selector):
        elements = self._element.xpath(selector)
        return ElementList([self.__class__(element, self) for element in elements])

    def find_by_name(self, name):
        elements = self._element.cssselect('[name="%s"]' % name)
        return ElementList([self.__class__(element, self) for element in elements])

    def find_by_tag(self, name):
        elements = self._element.cssselect(name)
        return ElementList([self.__class__(element, self) for element in elements])

    def find_by_value(self, value):
        elements = self._element.cssselect('[value="%s"]' % value)
        return ElementList([self.__class__(element, self) for element in elements])

    def find_by_id(self, id):
        elements = self._element.cssselect('#%s' % id)
        return ElementList([self.__class__(element, self) for element in elements])

    @property
    def value(self):
        return self._element.text

    @property
    def text(self):
        return self.value


# class ZombieTestBrowserLinkElement(ZombieTestBrowserElement):

#     def __init__(self, element, parent):
#         super(ZombieTestBrowserLinkElement, self).__init__(element, parent)
#         self._browser = parent._browser

#     def __getitem__(self, attr):
#         return super(ZombieTestBrowserLinkElement, self).__getitem__(attr)

#     def click(self):
#         return self._browser.visit(self["href"])


# class ZombieTestBrowserControlElement(ElementAPI):

#     def __init__(self, control, parent):
#         self._control = control
#         self.parent = parent

#     def __getitem__(self, attr):
#         return self._control.mech_control.attrs[attr]

#     @property
#     def value(self):
#         return self._control.value

#     @property
#     def checked(self):
#         return bool(self._control.value)

#     def click(self):
#         return self._control.click()


# class ZombieTestBrowserOptionElement(ElementAPI):

#     def __init__(self, control, parent):
#         self._control = control
#         self.parent = parent

#     def __getitem__(self, attr):
#         return self._control.mech_item.attrs[attr]

#     @property
#     def text(self):
#         return self._control.mech_item.get_labels()[0]._text

#     @property
#     def value(self):
#         return self._control.optionValue

#     @property
#     def selected(self):
#         return self._control.mech_item._selected

