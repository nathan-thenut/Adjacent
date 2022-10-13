#include <emscripten/bind.h>

#include "expression.hpp"
#include "entity.hpp"
#include "constraint.hpp"

using namespace emscripten;


EMSCRIPTEN_BINDINGS(adjacent_api)
{
    class_<Sketch>("Sketch")
        .constructor<>()
        .function("add_entity", &Sketch::add_entity)
        .function("remove_entity", &Sketch::remove_entity)
        .function("add_constraint", &Sketch::add_constraint)
        .function("remove_constraint", &Sketch::remove_constraint)
        .function("add_expression", &Sketch::add_expression)
        .function("remove_expression", &Sketch::remove_expression)
        .function("add_expressionVector", &Sketch::add_expressionVector)
        .function("remove_expressionVector", &Sketch::remove_expressionVector)
        .function("is_using_linear_program", &Sketch::is_using_linear_program)
        .function("use_linear_program", &Sketch::use_linear_program)
        .function("update", &Sketch::update);

    using Prm = Param<double>;
    class_<Prm>("Param")
        .smart_ptr_constructor("Param", &std::make_shared<Prm, std::string, double>)
        // .constructor<std::string, double>()
        .property("name", &Prm::m_name)
        .function("set_value", &Prm::set_value)
        .function("expr", &Prm::expr)
        .function("value", &Prm::value)
        .function("to_string", &Prm::to_string);

    class_<Entity>("Entity").smart_ptr<std::shared_ptr<Entity>>("Entity");

    register_vector<double>("VectorDouble");

    class_<PointE, base<Entity>>("Point")
        .smart_ptr_constructor("Point", &std::make_shared<PointE, ParamPtr, ParamPtr, ParamPtr>)
        // .constructor<ParamPtr, ParamPtr, ParamPtr>()
        .function("expr", &PointE::expr)
        // .function("eval",
        //      [](PointE& p) {
        //          return std::vector<double>({ p.x->value(), p.y->value() });
        //      })
        .function("to_string", &PointE::to_string)
        .function("to_vector", &PointE::to_vector)
        .function("drag_to", &PointE::drag_to);

    class_<LineE, base<Entity>>("Line")
        .smart_ptr_constructor("Line", &std::make_shared<LineE, PointE, PointE>)
        // .constructor<PointE, PointE>()
        .function("source", &LineE::source)
        .function("target", &LineE::target)
        // .def("expr", &LineE::expr)
        .function("to_string", &LineE::to_string);

    class_<CircleE, base<Entity>>("Circle")
        .smart_ptr_constructor("Circle", &std::make_shared<CircleE, PointE, ParamPtr>)
        // .constructor<PointE, ParamPtr>()
        .function("center", &CircleE::center)
        .function("radius", &CircleE::radius)
        .function("to_string", &CircleE::to_string)
        .function("drag_center_to", &CircleE::drag_center_to)
        .function("drag_radius_to", &CircleE::drag_radius_to);


    class_<Constraint>("Constraint").smart_ptr<std::shared_ptr<Constraint>>("Constraint");

    class_<ValueConstraint, base<Constraint>>("ValueConstraint")
        .smart_ptr<std::shared_ptr<ValueConstraint>>("ValueConstraint");

    class_<PointOnConstraint, base<ValueConstraint>>("PointOn").smart_ptr_constructor(
        "PointOn", &std::make_shared<PointOnConstraint, std::shared_ptr<PointE>, EntityPtr>);
    // .constructor<std::shared_ptr<PointE>, EntityPtr>();

    class_<LengthConstraint, base<ValueConstraint>>("Length").smart_ptr_constructor(
        "Length", &std::make_shared<LengthConstraint, EntityPtr, double>);
    // .constructor<EntityPtr, double>();

    class_<PointsCoincidentConstraint>("Coincident")
        .smart_ptr_constructor("Coincident",
                               &std::make_shared<PointsCoincidentConstraint,
                                                 std::shared_ptr<PointE>&,
                                                 std::shared_ptr<PointE>&>);
    // .constructor<std::shared_ptr<PointE>&, std::shared_ptr<PointE>&>();

    class_<PointsDistanceConstraint, base<ValueConstraint>>("Distance")
        .smart_ptr_constructor("Distance",
                               &std::make_shared<PointsDistanceConstraint,
                                                 std::shared_ptr<PointE>&,
                                                 std::shared_ptr<PointE>&,
                                                 double>);
    // .constructor<std::shared_ptr<PointE>&, std::shared_ptr<PointE>&, double>()
    // .constructor<std::shared_ptr<LineE>&, double>();

    class_<AngleConstraint, base<ValueConstraint>>("Angle").smart_ptr_constructor(
        "Angle",
        &std::
            make_shared<AngleConstraint, std::shared_ptr<LineE>&, std::shared_ptr<LineE>&, double>);
    // .constructor<std::shared_ptr<LineE>&, std::shared_ptr<LineE>&, double>();

    class_<DiameterConstraint, base<ValueConstraint>>("Diameter")
        .smart_ptr_constructor(
            "Diameter", &std::make_shared<DiameterConstraint, std::shared_ptr<Entity>&, double>);
    // .constructor<std::shared_ptr<Entity>&, double>();

    enum_<HVOrientation>("HVOrientation")
        .value("OX", HVOrientation::OX)
        .value("OY", HVOrientation::OY);

    class_<HVConstraint, base<Constraint>>("HV")
        .smart_ptr_constructor(
            "HV", &std::make_shared<HVConstraint, std::shared_ptr<LineE>, HVOrientation>)
        .constructor<std::shared_ptr<PointE>, std::shared_ptr<PointE>, HVOrientation>();
    // .constructor<std::shared_ptr<LineE>, HVOrientation>();

    class_<ParallelConstraint, base<Constraint>>("Parallel")
        .smart_ptr_constructor("Parallel",
                               &std::make_shared<ParallelConstraint,
                                                 std::shared_ptr<LineE>&,
                                                 std::shared_ptr<LineE>&>);
    // .constructor<std::shared_ptr<LineE>&, std::shared_ptr<LineE>&>();

    class_<OrthogonalConstraint, base<Constraint>>("Orthogonal")
        .smart_ptr_constructor("Orthogonal",
                               &std::make_shared<OrthogonalConstraint,
                                                 std::shared_ptr<LineE>&,
                                                 std::shared_ptr<LineE>&>);


    class_<TangentConstraint, base<Constraint>>("Tangent").smart_ptr_constructor(
        "Tangent",
        &std::make_shared<TangentConstraint, std::shared_ptr<CircleE>&, std::shared_ptr<LineE>&>);
    // .constructor<std::shared_ptr<CircleE>&, std::shared_ptr<LineE>&>();

    class_<Expr>("Expr")
        .smart_ptr_constructor("Expr", &std::make_shared<Expr, double>)
        // .constructor<double>()
        .function("eval", &Expr::eval)
        .function("to_string", &Expr::to_string)
        .function("drag", &Expr::drag);

    class_<ExpVector>("ExprVector")
        .smart_ptr_constructor("ExpVector",
                               &std::make_shared<ExpVector,
                                                 std::shared_ptr<Expr>&,
                                                 std::shared_ptr<Expr>&,
                                                 std::shared_ptr<Expr>&>)
        // .function("to_string", [](ExpVector& self) -> std::string {
        //     std::string res = "{\n";
        //     res += self.x->to_string() + "\n";
        //     res += self.y->to_string() + "\n";
        //     res += self.z->to_string() + "\n";
        //     res += "}";
        //     return res;
        // })
        ;
}
