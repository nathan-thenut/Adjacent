emcc ../src/expression.cpp ../src/expression_vector.cpp ../src/gaussian_method.cpp ../src/equation_system.cpp ../src/expr_basis.cpp -I/home/ugo/lib/xtl/include -I/home/ugo/lib/xtensor/include -I../include -c
emar rcs libtest.a equation_system.o expr_basis.o expression_vector.o expression.o gaussian_method.o
emcc -lembind -o lib.js ../src/js_interface.cpp -I/home/ugo/lib/xtl/include -I/home/ugo/lib/xtensor/include -I../include -Wl,--whole-archive libtest.a -Wl,--no-whole-archive
