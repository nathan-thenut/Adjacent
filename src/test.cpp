#include <iostream>
#include "expression.hpp"
#include "entity.hpp"
#include "constraint.hpp"


int main()
{
    auto a = expr(123);
    auto b = expr(323);
    auto p = param("test", 1.);
    auto c = (a + sin(b) * sin(p->expr()));
    std::cout << (a + sin(b) * sin(p->expr()))->to_string() << std::endl;

    std::cout << c->d(p)->to_string() << std::endl;
    std::cout << "Hello world." << std::endl;

    auto p1 = std::make_shared<PointE>(param("p1_x", 3), param("p1_y", 1), param("p1_z", 1));
    auto p2 = std::make_shared<PointE>(param("p2_x", 4), param("p2_y", 2), param("p2_z", 1));
    auto p3 = std::make_shared<PointE>(param("p3_x", 10.5), param("p3_y", 1.5), param("p3_z", 1));
    auto p4 = std::make_shared<PointE>(param("p4_x", 10.5), param("p4_y", 1.5), param("p4_z", 1));

    auto l = std::make_shared<LineE>(*p1, *p2);
    auto l1 = std::make_shared<LineE>(*p3, *p4);

    std::cout << l->to_string() << std::endl;
    std::cout << p3->to_string() << std::endl;

    Sketch s;
    s.add_entity(p1);
    s.add_entity(p2);
    s.add_entity(p3);
    s.add_entity(p4);
    // s.add_entity(l);
    // s.add_entity(l1);

    //
    // std::cout << "Adding Point On" << std::endl;
    // auto ccc = std::make_shared<PointOnConstraint>(p3, l);
    // s.add_constraint(ccc);
    // s.update();
    // s.sys.solve();
    // std::cout << "Adding length" << std::endl;
    // auto lC = std::make_shared<PointsDistanceConstraint>(p1, p2, 15);
    // s.add_constraint(lC);
    // s.update();
    // s.sys.solve();

    // auto lC1 = std::make_shared<EqualConstraint>(l, l1, 2);
    // s.add_constraint(lC1);
    // s.update();
    // s.sys.solve();

    // std::cout << "Adding HV Constraint" << std::endl;
    // auto HC = std::make_shared<HVConstraint>(l, OX);
    // s.add_constraint(HC);
    // s.update();
    // s.sys.solve();

    // auto HC1 = std::make_shared<HVConstraint>(l1, OX);
    // s.add_constraint(HC1);
    // s.update();
    // s.sys.solve();

    auto param_x = param("drag_x", 5.);
    auto param_y = param("drag_y", 0.);
    auto param_z = param("drag_z", 1.);
    auto vec = std::make_shared<ExpVector>(param_x->expr(), param_y->expr(), param_z->expr());
    auto ddd = p4->drag_to(vec);
    s.add_expressionVector(ddd);
    s.update();
    param_x->set_value(3.);
    param_y->set_value(3.);
    param_z->set_value(1.);
    s.update();
    // std::cout << s.sys.solve() << std::endl;

    int rank;
    s.sys.test_rank(rank);

    std::cout << "RANK: " << rank << std::endl;

    for (auto& el : s.entities)
    {
        std::cout << el->to_string() << std::endl;
    }


    return 0;
}
