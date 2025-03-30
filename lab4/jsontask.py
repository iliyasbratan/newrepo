import json

file = open("Lab 04/sample-data.json", "r")
data = file.read()
parsed = json.loads(data)

# print(parsed)

imdata = parsed["imdata"]

def is_valid_record(record):
  try:
    attr = record["l1PhysIf"]["attributes"]
    dn = attr["dn"]
    ethNum = int(dn[dn.rfind("/") + 1:dn.rfind("]")])
    return 33 <= ethNum <= 35
  except:
    return False


interface_len = 80
dn_pad = 50
descr_pad = 20
speed_pad = 6
mtu_pad = 5

dn_key = "dn"
descr_key = "descr"
speed_key = "speed"
mtu_key = "mtu"

dn_header = "DN"
descr_header = "Description"
speed_header = "Speed"
mtu_header = "MTU"

print("Interface Status")
print("=" * interface_len)

print(
  dn_header.ljust(dn_pad),
  descr_header.ljust(descr_pad),
  speed_header.ljust(speed_pad),
  mtu_header.ljust(mtu_pad)
)
print(
  "-" * dn_pad,
  "-" * descr_pad,
  "-" * speed_pad,
  "-" * mtu_pad
)

for record in imdata:
  if not is_valid_record(record):
    continue
  
  attr = record["l1PhysIf"]["attributes"]

  print(
    attr[dn_key].ljust(dn_pad),
    attr[descr_key].ljust(descr_pad),
    attr[speed_key].ljust(speed_pad),
    attr[mtu_key].ljust(mtu_pad)
  )
