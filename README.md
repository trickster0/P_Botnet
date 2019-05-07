# P_Botnet
Private Botnet I made for the fun of it in pure python.
This botnet is using dynamic AES encryption per command over SSL.
<p>
For the encryption to work, you are going to have to use the script i provided to create a pair of keys.
The project still needs a few tweaks here and there.

<IMG SRC="https://raw.githubusercontent.com/trickster0/P_Botnet/master/botnet.png"/>
On the server side -
<strong>USAGE:</strong>
<p>
<pre><code>python server.py
</code></pre>

On the client site - 
<strong>USAGE:</strong>
<p>
<pre><code>python client.py
</code></pre>


Changing the IP in the client.py might be needed depending on your situation.
Library pyxhook is also needed for this project, for keylogging purposes
To install : pip2.7 install pyxhook

Author: Thanasis Tserpelis aka trickster0

|| Copyright 2017 (License) ||

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
