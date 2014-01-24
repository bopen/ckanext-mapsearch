
def div(a, b):
    return a / b


def mul(a, b):
    return a * b


def add(a, b):
    return a + b


def sub(a, b):
    return a - b


def calc(minx, miny, maxx, maxy):
    return div(
               mul(
                  mul(
                      max(
                          0,
                             sub(
                                 min(19.5666503906, maxx),
                                 max(5.41625976562, minx)
                             )
                      ),
                      max(
                          0,
                          sub(
                              min(49.3465988483, maxy),
                              max(44.4965053311, miny)
                          )
                      )
                  ),
                  2
              ),
              add(
                 68.6307178367,
                 mul(
                     sub(maxy,miny),
                     sub(maxx,minx)
                 )
              )
          )

if __name__ == '__main__':
    print calc(1,1,100,100)

