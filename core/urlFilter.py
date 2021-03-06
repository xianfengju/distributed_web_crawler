from robotparser import RobotFileParser
from urlparse import urljoin
import mimetypes
import urllib2
import hashlib
from threading import Lock
from datetime import datetime


class RobotFilter(object):
	"""
	TO BE DONE
	"""
	def __init__(self, userAgent):
		self._userAgent = userAgent
		self._dict = {}
		
	def disallow(self, url):
		"""
		TO BE DONE
		"""
		robotFile = urljoin(url, "/robots.txt")
		# key = hashlib.sha1(robotFile).hexdigest()
		if(not self._dict.has_key(key)):
			self._dict[key] = RobotFileParser(robotFile)
			try:
				self._dict[key].read()
			except :
				self._dict[key] = None
		result = self._dict[key] is None or not self._dict[key].can_fetch(self._userAgent, url)
		return result
		
	
class FileTypeFilter(object):
 	"""
 	TO BE DONE
 	"""
 	def __init__(self, allowOrDisallow = True, filterList = None):
 		self._allow = allowOrDisallow
 		self._filterList = filterList if filterList else []

 	def disallow(self, url):
		"""
		TO BE DONE
		"""
		fileType = mimetypes.guess_type(url)[0]
		if(self._allow == (fileType in self._filterList)):
			return False
		try:
			return not url.endswith(urllib2.Request(url).get_host()) and not url.endswith(urllib2.Request(url).get_host()+'/')
		except:
			return True

class DupEliminator(object):
	"""
	A URLValidator is used to validate urls.
	"""
	def __init__(self):
		self._visited = set()
		self._lock = Lock()
		
	def seenBefore(self, url):
		"""
		Check if a given url has been visited before.
		---------  Param --------
		url: (str)  		
			The url to be checked.
		---------  Return --------
		(bool): True if url has been visited before, false otherwise.
		"""
		self._lock.acquire()
		try:	
			# url = hashlib.sha1(url).hexdigest()
			visited = url in self._visited
			if(not visited):
				self._visited.add(url)
			return visited
		finally:
			self._lock.release() 

	def size(self):
		"""
		Return the number of downloaded pages so far.
		"""
		self._lock.acquire()
		try:	
			total = len(self._visited)
			return total
		finally:
			self._lock.release()
