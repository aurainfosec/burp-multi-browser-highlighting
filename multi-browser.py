from burp import IBurpExtender
from burp import IHttpListener	
from burp import IProxyListener
from burp import IInterceptedProxyMessage
from java.io import PrintWriter
class BurpExtender(IBurpExtender,IProxyListener):
	def registerExtenderCallbacks( self, callbacks):
		# keep a reference to our callbacks and helper object
		self._callbacks=callbacks
		self._helpers=callbacks.getHelpers()

		self.stdout = PrintWriter(callbacks.getStdout(), True)

		# Keep Track of Browsers
		self._browser={}
		# Colors for different browsers
		self.colors=["red", "pink", "green","magenta","cyan", "gray", "yellow",None]
 
		
		self._callbacks.setExtensionName("Multi-Browser")
		
		#IExtensionHelpers helpers = callbacks.getHelpers()
		callbacks.registerProxyListener(self)
		return

	def processProxyMessage(self, messageIsRequest, message):
		#	self._stdout.println(("Proxy request to " if messageIsRequest else "Proxy response from ") + message.getMessageInfo().getHttpService().toString())
		if messageIsRequest == False:
			return
		browser_agent=None
		headers=self._helpers.analyzeRequest(message.getMessageInfo()).getHeaders()
		for x in headers:
			if x.lower().startswith("user-agent:"):
				browser_agent=x
				break

		if browser_agent not in self._browser:
			self._browser[browser_agent]={"id":len(self._browser)+1, "agent":browser_agent, "color":self.colors.pop()}


		self.stdout.println(self._browser[browser_agent]["agent"])
		message.getMessageInfo().setHighlight(self._browser[browser_agent]["color"])
