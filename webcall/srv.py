import http.server, os, urllib.request, json
class H(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        r=urllib.request.Request("https://api.bolna.ai/web-call/session",method="POST",data=json.dumps({"agent_id":os.environ["AID"]}).encode(),headers={"Authorization":"Bearer "+os.environ["BOLNA_API_KEY"],"Content-Type":"application/json"})
        b=urllib.request.urlopen(r).read(); open("run_id.txt","w").write(json.loads(b)["run_id"])
        self.send_response(200);self.send_header("Content-Type","application/json");self.end_headers();self.wfile.write(b)
    def log_message(self,*a):pass
http.server.ThreadingHTTPServer(("127.0.0.1",8765),H).serve_forever()
